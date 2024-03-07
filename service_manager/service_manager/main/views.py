import datetime
from io import BytesIO
from django.db.models import F
from django.conf import settings
from django.contrib.auth.decorators import permission_required
from django.core.exceptions import ValidationError
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
import django.views.generic as views
from django.template.defaultfilters import slugify
from django.urls import reverse_lazy, reverse
from django.contrib.auth import mixins as auth_mixins

from service_manager.core.mixins import MaterialFilteringMixin
from service_manager.core.utils import get_protocol_and_domain_as_string, get_material_count_matching_conditions
from service_manager.customers.models import CustomerRepresentative
from service_manager.main.forms import CreateServiceOrderHeaderForm, CreateServiceOrderDetailForm, \
    EditServiceOrderDetailForm, CreateServiceOrderNoteForm, HandoverServiceOrderForm, ContactForm, TrackOrderSearchForm, \
    CreateCustomerNotificationForm
from service_manager.main.models import Customer, CustomerAsset, ServiceOrderHeader, ServiceOrderDetail, \
    ServiceOrderNote, CustomerNotification, ServiceRequest
from service_manager.main.tasks import send_contact_us_email
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from weasyprint import HTML, CSS
import qrcode
import qrcode.image.svg

from service_manager.master_data.forms import FilterMaterialForm
from service_manager.master_data.models import Material


class HomeTemplateView(views.TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Service requests
        open_service_requests = ServiceRequest.objects.all().filter(status__in=[1, 2, 3]).order_by('-created_on')
        open_service_requests_count = open_service_requests.count()
        open_service_requests = open_service_requests[:3]

        # Pending service orders
        pending_service_orders = ServiceOrderHeader.objects.all().filter(is_serviced=False).order_by('-created_on')
        pending_service_orders_count = pending_service_orders.count()
        pending_service_orders = pending_service_orders[:3]

        # Completed service orders
        completed_service_orders = ServiceOrderHeader.objects.all().filter(
            Q(is_serviced=True) & Q(is_completed=False)).order_by('-created_on')
        completed_service_orders_count = completed_service_orders.count()
        completed_service_orders = completed_service_orders[:3]

        context['open_service_requests'] = open_service_requests
        context['open_service_requests_count'] = open_service_requests_count

        context['pending_service_orders'] = pending_service_orders
        context['pending_service_orders_count'] = pending_service_orders_count

        context['completed_service_orders'] = completed_service_orders
        context['completed_service_orders_count'] = completed_service_orders_count

        return context


class ServiceOrderHeaderListBaseView(auth_mixins.PermissionRequiredMixin, views.ListView):
    RELATED_ENTITIES = ['serviceordernote_set', 'serviceorderdetail_set', 'customer']

    model = ServiceOrderHeader
    template_name = 'service_order_header/list_views/service_orders_service.html'
    ordering = (
        'service_level_agreement', 'customer__has_subscription', 'customer__is_regular_customer', 'created_on',
        'customer')
    context_object_name = 'service_orders'
    paginate_by = 10
    permission_required = 'main.view_serviceorderheader'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.order_by(
            F('service_level_agreement__id').desc(nulls_last=True),
            '-customer__has_subscription',
            '-customer__is_regular_customer',
            'created_on'
        )
        return queryset


class ServiceOrderHeaderPendingServiceListView(ServiceOrderHeaderListBaseView):
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(is_serviced=False).prefetch_related(*self.RELATED_ENTITIES)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Pending Service Orders')
        return context


class ServiceOrderHeaderServicedListView(ServiceOrderHeaderListBaseView):
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(Q(is_serviced=True) & Q(is_completed=False)).prefetch_related(*self.RELATED_ENTITIES)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = _('Completed Service Orders')
        return context


class ServiceOrderHeaderDetailView(auth_mixins.PermissionRequiredMixin, views.DetailView):
    model = ServiceOrderHeader
    template_name = 'service_order_header/core/service_order_details.html'
    context_object_name = 'service_order_header'

    permission_required = 'main.view_serviceorderheader'

    # Override the queryset in order to include the (soft) deleted SOHs
    # This is needed when showing the service history of a given Customer Asset
    def get_queryset(self, *args, **kwargs):
        queryset = ServiceOrderHeader.all_records.all()
        return queryset


class CreateServiceOrderHeader(auth_mixins.PermissionRequiredMixin, views.CreateView):
    model = ServiceOrderHeader
    form_class = CreateServiceOrderHeaderForm
    template_name = 'service_order_header/core/service_order_create.html'

    permission_required = 'main.add_serviceorderheader'

    def get(self, request, *args, **kwargs):

        if 'service_request_id' in self.request.GET:
            self.kwargs['service_request_id'] = self.request.GET['service_request_id']

        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse_lazy(
            'create_service_order_success',
            kwargs=
            {
                'pk': self.object.id,
            }
        )

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['customer_id'] = self.kwargs['customer_id']
        return kwargs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        customer_id = self.kwargs['customer_id']
        customer_asset_id = self.kwargs['asset_id']

        if customer_id:
            customer = Customer.objects.get(pk=customer_id)
            context['customer'] = customer
        if customer_asset_id:
            customer_asset = CustomerAsset.objects.get(pk=customer_asset_id)
            context['customer_asset'] = customer_asset

        return context

    def form_valid(self, form):
        customer_id = self.kwargs['customer_id']
        customer_asset_id = self.kwargs['asset_id']

        service_order = form.save(commit=False)
        service_order.accepted_by = self.request.user
        service_order.customer = Customer.objects.get(pk=customer_id)
        service_order.customer_asset = CustomerAsset.objects.get(pk=customer_asset_id)

        # Update the Service request if applicable
        if 'service_request_id' in self.request.GET:
            service_request_id = self.request.GET['service_request_id']
            service_request = ServiceRequest.objects.get(pk=service_request_id)
            # todo: make this exception better
            if service_request.customer != service_order.customer:
                raise ValidationError('Service request customer is different from the Service order customer!')
            service_request.service_order = service_order
            service_order.save()
            service_request.save()
        else:
            service_order.save()

        # Create a slug
        created_on = service_order.created_on
        slug = f'{hex(service_order.pk)}-{hex(created_on.year)}-{hex(created_on.month)}-{hex(created_on.day)}'
        service_order.slug = slugify(slug)

        return super().form_valid(form)


class CreateServiceOrderSuccess(auth_mixins.PermissionRequiredMixin, views.DetailView):
    model = ServiceOrderHeader
    context_object_name = 'service_order'
    template_name = 'service_order_header/create_service_order_header_success.html'
    permission_required = 'main.view_serviceorderheader'


class DeleteServiceOrderHeaderView(auth_mixins.PermissionRequiredMixin, views.DeleteView):
    model = ServiceOrderHeader
    template_name = 'service_order_header/core/service_order_delete.html'
    success_url = reverse_lazy('service_orders_list_pending_service')

    permission_required = 'main.change_serviceorderheader'


class CreateServiceOrderDetailView(MaterialFilteringMixin, auth_mixins.PermissionRequiredMixin, views.CreateView):
    model = ServiceOrderDetail
    template_name = 'service_order_detail/service_order_details_create.html'
    form_class = CreateServiceOrderDetailForm

    permission_required = 'main.add_serviceorderdetail'

    def get_success_url(self):
        service_order_header_id = self.kwargs['order_id']
        return reverse_lazy('create_service_order_detail', kwargs={'order_id': service_order_header_id})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['filter_form'] = FilterMaterialForm(self.request.GET or None)

        service_order_header_id = self.kwargs['order_id']
        if service_order_header_id:
            context['service_order_header'] = ServiceOrderHeader.objects.prefetch_related(
                'serviceorderdetail_set').get(pk=int(service_order_header_id))

        context['material_count'] = get_material_count_matching_conditions(
            self.request.GET.get('category' or None),
            self.request.GET.get('search' or None)
        )

        return context

    def form_valid(self, form):
        service_order_header_id = self.kwargs['order_id']
        service_order_header = ServiceOrderHeader.objects.get(pk=service_order_header_id)
        service_order_detail = form.save(commit=False)

        service_order_detail.service_order = service_order_header
        service_order_detail.save()

        return super().form_valid(form)


class EditServiceOrderDetailView(auth_mixins.PermissionRequiredMixin, views.UpdateView):
    model = ServiceOrderDetail
    template_name = 'service_order_detail/service_order_detail_edit.html'
    form_class = EditServiceOrderDetailForm

    permission_required = 'main.change_serviceorderdetail'

    def get_success_url(self):
        service_order_header_id = self.kwargs['order_id']
        if service_order_header_id:
            return reverse_lazy('create_service_order_detail', kwargs={'order_id': service_order_header_id})
        return reverse_lazy('service_orders_list')


class ServiceOrderDetailsListView(auth_mixins.PermissionRequiredMixin, views.ListView):
    model = ServiceOrderDetail
    template_name = 'service_order_detail/service_order_details.html'
    ordering = ('material', 'quantity',)

    permission_required = 'main.view_serviceorderdetail'


class DeleteServiceOrderDetailView(auth_mixins.PermissionRequiredMixin, views.DeleteView):
    model = ServiceOrderDetail
    template_name = 'service_order_detail/service_order_detail_delete.html'

    permission_required = 'main.change_serviceorderdetail'

    def get_success_url(self):
        service_order_header_id = self.kwargs['order_id']
        if service_order_header_id:
            return reverse_lazy('create_service_order_detail', kwargs={'order_id': service_order_header_id})
        return reverse_lazy('service_orders_list')


@permission_required('main.change_serviceorderheader')
def complete_service_order(request, pk):
    service_order_header = ServiceOrderHeader.objects.get(pk=pk)
    service_order_header.is_serviced = True
    service_order_header.serviced_by = request.user
    service_order_header.serviced_on = datetime.datetime.now()
    service_order_header.save()

    return redirect('service_orders_list_pending_service')


class CreateServiceOrderNoteView(auth_mixins.PermissionRequiredMixin, views.CreateView):
    model = ServiceOrderNote
    template_name = 'service_order_note/service_order_note_create.html'
    form_class = CreateServiceOrderNoteForm

    permission_required = 'main.add_serviceordernote'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        service_order_id = self.kwargs['order_id']
        if service_order_id:
            service_order = ServiceOrderHeader.objects.filter(pk=service_order_id).get()
            context['service_order'] = service_order

        return context

    def get_success_url(self):
        go_to_next = self.request.POST.get('next', '/')
        return go_to_next

    def form_valid(self, form):
        service_order_id = self.kwargs['order_id']
        service_order_header = ServiceOrderHeader.objects.get(pk=service_order_id)

        note = form.save(commit=False)
        note.service_order = service_order_header
        note.created_by = self.request.user
        note.save()

        return super().form_valid(form)


class ServiceOrderNotesListView(auth_mixins.PermissionRequiredMixin, views.ListView):
    model = ServiceOrderNote
    template_name = 'service_order_note/service_order_notes.html'

    permission_required = 'main.view_serviceordernote'


class ServiceOrderNoteDetailView(auth_mixins.PermissionRequiredMixin, views.DetailView):
    model = ServiceOrderNote
    template_name = 'service_order_note/service_order_note_detail.html'

    permission_required = 'main.view_serviceordernote'


class EditServiceOrderNoteView(auth_mixins.PermissionRequiredMixin, views.UpdateView):
    model = ServiceOrderNote
    template_name = 'service_order_note/service_order_note_edit.html'
    form_class = CreateServiceOrderNoteForm

    permission_required = 'main.change_serviceordernote'

    def get_success_url(self):
        go_to_next = self.request.POST.get('next', '/')
        return go_to_next


class DeleteServiceOrderNoteView(auth_mixins.PermissionRequiredMixin, views.DeleteView):
    model = ServiceOrderNote
    template_name = 'service_order_note/service_order_note_delete.html'

    permission_required = 'main.change_serviceordernote'

    def get_success_url(self):
        go_to_next = self.request.POST.get('next', '/')
        return go_to_next


@permission_required('main.change_serviceorderheader')
def rollback_service_order(request, pk):
    service_order_header = ServiceOrderHeader.objects.get(pk=pk)
    service_order_header.is_serviced = False
    service_order_header.serviced_by = None
    service_order_header.serviced_on = None
    service_order_header.save()

    return redirect('service_orders_list_pending_service')


class HandoverServiceOrderView(auth_mixins.PermissionRequiredMixin, views.UpdateView):
    model = ServiceOrderHeader
    form_class = HandoverServiceOrderForm
    template_name = 'service_order_header/core/service_order_handover.html'

    permission_required = 'main.change_serviceorderheader'

    def get_initial(self):
        initial = super().get_initial()
        service_order_header_id = self.kwargs['pk']

        if service_order_header_id:
            initial.update({'service_order': service_order_header_id})

            service_order_header = ServiceOrderHeader.objects.get(pk=service_order_header_id)
            representatives = CustomerRepresentative.objects.filter(customer=service_order_header.customer_id)

            if representatives.exists():
                initial['handed_over_to'] = representatives.first()

        return initial

    def form_valid(self, form):
        service_oder = form.save(commit=False)

        service_oder.is_completed = True
        service_oder.completed_by = self.request.user
        service_oder.completed_on = datetime.datetime.now()
        service_oder.save()

        return super().form_valid(form)

    def get_success_url(self):
        order_id = self.kwargs['pk']
        return reverse_lazy('detail_service_order', kwargs={'pk': order_id})


def contact_us(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            email_data = {
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'email_address': form.cleaned_data['email_address'],
                'message': form.cleaned_data['message'],
            }
            send_contact_us_email.delay(email_data)
            messages.success(request, _("The email message was sent."))
            return redirect('index')
        else:
            for key, error in list(form.errors.items()):
                if key == 'captcha' and error[0] == 'This field is required.':
                    messages.error(request, "You must pass the reCAPTCHA test")
                    continue
                messages.error(request, error)

    form = ContactForm()
    context = {
        'form': form,
    }
    return render(request, 'contact_us.html', context)


class TrackOrderDetailView(views.DetailView):
    model = ServiceOrderHeader
    template_name = 'service_order_header/service_order_track.html'
    context_object_name = 'order'


class ServiceOrderPrintoutView(views.DetailView):
    template_name = 'service_order_header/customer_printout.html'
    model = ServiceOrderHeader
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Generate the link in the QR code
        domain = get_protocol_and_domain_as_string()
        code_text = f"{domain}{reverse('track_order', kwargs={'slug': kwargs['object'].slug})}"

        # Build the QR code
        factory = qrcode.image.svg.SvgImage
        img = qrcode.make(code_text, image_factory=factory, box_size=5)

        # Save as stream
        stream = BytesIO()
        img.save(stream)

        # Pass to the context
        context["qrcode"] = stream.getvalue().decode()
        return context

    def get(self, request, *args, **kwargs):
        template_response = super().get(self, request, *args, **kwargs)
        styles = CSS(settings.STATIC_ROOT + "/css/main.css")
        html = HTML(string=template_response.rendered_content).write_pdf(
            stylesheets=[
                styles,
            ]
        )

        response = HttpResponse(html, content_type='application/pdf')

        response['Content-Disposition'] = f'filename=Customer_Printout_{kwargs["pk"]}.pdf'
        return response


class TrackOrderSearchFormView(views.FormView):
    template_name = 'service_order_header/service_order_track_search.html'
    form_class = TrackOrderSearchForm

    def form_valid(self, form):
        order_slug = form.cleaned_data['order_tracking_number'].strip().lower()
        service_order = ServiceOrderHeader.objects.filter(slug__exact=order_slug)

        if not service_order:
            messages.error(self.request, _("Invalid Tracking number!"))
            return self.render_to_response(self.get_context_data(request=self.request, form=form))
        else:
            self.success_url = reverse('track_order', kwargs={'slug': order_slug})
            return super().form_valid(form)

    def form_invalid(self, form):
        for key, error in list(form.errors.items()):
            if key == 'captcha' and error[0] == 'This field is required.':
                messages.error(self.request, "You must pass the reCAPTCHA test")
                continue
            messages.error(self.request, error)
        return self.render_to_response(self.get_context_data(request=self.request, form=form))


class CustomerNotificationsListView(auth_mixins.PermissionRequiredMixin, views.ListView):
    model = CustomerNotification
    template_name = 'customer_notification/customer_notifications.html'

    # todo: create a new permission and change here and in the template as well
    permission_required = 'main.view_serviceordernote'


class CreateCustomerNotificationView(auth_mixins.PermissionRequiredMixin, views.CreateView):
    model = CustomerNotification
    template_name = 'customer_notification/customer_notification_create.html'
    form_class = CreateCustomerNotificationForm

    # todo: create a new permission and change here and in the template as well
    permission_required = 'main.add_serviceordernote'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        service_order_id = self.kwargs['order_id']
        if service_order_id:
            service_order = ServiceOrderHeader.objects.filter(pk=service_order_id).get()
            context['service_order'] = service_order

        return context

    def get_success_url(self):
        go_to_next = self.request.POST.get('next', '/')
        return go_to_next

    def form_valid(self, form):
        service_order_id = self.kwargs['order_id']
        service_order_header = ServiceOrderHeader.objects.get(pk=service_order_id)

        notification = form.save(commit=False)
        notification.service_order = service_order_header
        notification.notified_by = self.request.user
        notification.notification_method = CustomerNotification.TYPE_CHOICE_PHONE
        notification.service_order_current_status = service_order_header.status
        notification.save()

        return super().form_valid(form)


class EditCustomerNotificationView(auth_mixins.PermissionRequiredMixin, views.UpdateView):
    model = CustomerNotification
    template_name = 'customer_notification/customer_notification_edit.html'
    form_class = CreateCustomerNotificationForm

    permission_required = 'main.change_serviceordernote'

    def get_success_url(self):
        go_to_next = self.request.POST.get('next', '/')
        return go_to_next


class DeleteCustomerNotificationView(auth_mixins.PermissionRequiredMixin, views.DeleteView):
    model = CustomerNotification
    template_name = 'customer_notification/customer_notification_delete.html'

    permission_required = 'main.change_serviceordernote'

    def get_success_url(self):
        go_to_next = self.request.POST.get('next', '/')
        return go_to_next


class CustomerNotificationDetailView(auth_mixins.PermissionRequiredMixin, views.DetailView):
    model = CustomerNotification
    template_name = 'customer_notification/customer_notification_detail.html'

    permission_required = 'main.view_serviceordernote'
