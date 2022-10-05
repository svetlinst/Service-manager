import datetime

from django.db.models import Q
from django.shortcuts import render, redirect
import django.views.generic as views
from django.urls import reverse_lazy
from django.contrib.auth import mixins as auth_mixins

from service_manager.main.forms import CreateServiceOrderHeaderForm, CreateServiceOrderDetailForm, \
    EditServiceOrderDetailForm, CreateServiceOrderNoteForm, HandoverServiceOrderForm
from service_manager.main.models import Customer, CustomerAsset, ServiceOrderHeader, ServiceOrderDetail, \
    ServiceOrderNote


def get_index(request):
    return render(request, 'index.html')


class ServiceOrderHeaderPendingServiceListView(auth_mixins.LoginRequiredMixin, views.ListView):
    model = ServiceOrderHeader
    template_name = 'service_order_header/list_views/service_orders_service.html'
    ordering = ('created_on', 'customer')
    RELATED_ENTITIES = ['serviceordernote_set', 'serviceorderdetail_set', ]

    def get_queryset(self):
        return ServiceOrderHeader.objects.filter(is_serviced=False).prefetch_related(*self.RELATED_ENTITIES)


class ServiceOrderHeaderServicedListView(ServiceOrderHeaderPendingServiceListView):
    template_name = 'service_order_header/list_views/service_orders_complete.html'
    ordering = ('serviced_on', 'customer')

    def get_queryset(self):
        return ServiceOrderHeader.objects.filter(Q(is_serviced=True) & Q(is_completed=False)).prefetch_related(
            *self.RELATED_ENTITIES)


class ServiceOrderHeaderDetailView(auth_mixins.LoginRequiredMixin, views.DetailView):
    model = ServiceOrderHeader
    template_name = 'service_order_header/core/service_order_details.html'
    context_object_name = 'service_order_header'


class CreateServiceOrderHeader(auth_mixins.LoginRequiredMixin, views.CreateView):
    model = ServiceOrderHeader
    form_class = CreateServiceOrderHeaderForm
    template_name = 'service_order_header/core/service_order_create.html'

    def get_success_url(self):
        return reverse_lazy('detail_service_order', kwargs={'pk': self.object.id})

    def get_initial(self):
        customer_id = self.kwargs['customer_id']
        customer_asset_id = self.kwargs['asset_id']
        if customer_id:
            self.initial.update({
                'customer': customer_id,
            })
        if customer_id:
            self.initial.update({
                'customer_asset': customer_asset_id,
            })

        user = self.request.user

        if user:
            self.initial.update({
                'accepted_by': user,
            })
        return super().get_initial()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        customer_id = self.kwargs['customer_id']
        customer_asset_id = self.kwargs['asset_id']

        if customer_id:
            customer = Customer.objects.filter(pk=customer_id).get()
            context['customer'] = customer
        if customer_asset_id:
            customer_asset = CustomerAsset.objects.filter(pk=customer_asset_id).get()
            context['customer_asset'] = customer_asset

        return context


class DeleteServiceOrderHeaderView(auth_mixins.LoginRequiredMixin, views.DeleteView):
    model = ServiceOrderHeader
    template_name = 'service_order_header/core/service_order_delete.html'
    success_url = reverse_lazy('service_orders_list_pending_service')


class CreateServiceOrderDetailView(auth_mixins.LoginRequiredMixin, views.CreateView):
    model = ServiceOrderDetail
    template_name = 'service_order_detail/service_order_details_create.html'
    form_class = CreateServiceOrderDetailForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        service_order_header_id = self.kwargs['order_id']
        if service_order_header_id:
            context['service_order_header'] = ServiceOrderHeader.objects.prefetch_related(
                'serviceorderdetail_set').filter(pk=int(service_order_header_id)).get()

        return context

    def form_valid(self, form):
        service_order_header_id = self.kwargs['order_id']
        service_order_header = ServiceOrderHeader.objects.filter(pk=service_order_header_id).get()
        service_order_detail = ServiceOrderDetail(
            quantity=form.cleaned_data['quantity'],
            discount=form.cleaned_data['discount'],
            material=form.cleaned_data['material'],
            service_order=service_order_header,
        )
        service_order_detail.save()

        return redirect('create_service_order_detail', service_order_header_id)


class EditServiceOrderDetailView(auth_mixins.LoginRequiredMixin, views.UpdateView):
    model = ServiceOrderDetail
    template_name = 'service_order_detail/service_order_detail_edit.html'
    form_class = EditServiceOrderDetailForm

    def get_success_url(self):
        service_order_header_id = self.kwargs['order_id']
        if service_order_header_id:
            return reverse_lazy('create_service_order_detail', kwargs={'order_id': service_order_header_id})
        return reverse_lazy('service_orders_list')


class ServiceOrderDetailsListView(auth_mixins.LoginRequiredMixin, views.ListView):
    model = ServiceOrderDetail
    template_name = 'service_order_detail/service_order_details.html'
    ordering = ('material', 'quantity',)


class DeleteServiceOrderDetailView(auth_mixins.LoginRequiredMixin, views.DeleteView):
    model = ServiceOrderDetail
    template_name = 'service_order_detail/service_order_detail_delete.html'

    def get_success_url(self):
        service_order_header_id = self.kwargs['order_id']
        if service_order_header_id:
            return reverse_lazy('create_service_order_detail', kwargs={'order_id': service_order_header_id})
        return reverse_lazy('service_orders_list')


def complete_service_order(request, pk):
    service_order_header = ServiceOrderHeader.objects.get(pk=pk)
    service_order_header.is_serviced = True
    service_order_header.serviced_by = request.user
    service_order_header.serviced_on = datetime.datetime.now()
    service_order_header.save()

    return redirect('service_orders_list_pending_service')


class CreateServiceOrderNoteView(auth_mixins.LoginRequiredMixin, views.CreateView):
    model = ServiceOrderNote
    template_name = 'service_order_note/service_order_note_create.html'
    form_class = CreateServiceOrderNoteForm

    def get_initial(self):
        user = self.request.user

        service_order_header_id = self.kwargs['order_id']

        if service_order_header_id:
            self.initial.update({
                'service_order': service_order_header_id,
            })

        if user:
            self.initial.update({
                'created_by': user,
            })

        return super().get_initial()

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


class ServiceOrderNotesListView(auth_mixins.LoginRequiredMixin, views.ListView):
    model = ServiceOrderNote
    template_name = 'service_order_note/service_order_notes.html'


class EditServiceOrderNoteView(auth_mixins.LoginRequiredMixin, views.UpdateView):
    model = ServiceOrderNote
    template_name = 'service_order_note/service_order_note_edit.html'
    form_class = CreateServiceOrderNoteForm

    def get_success_url(self):
        go_to_next = self.request.POST.get('next', '/')
        return go_to_next


class DeleteServiceOrderNoteView(auth_mixins.LoginRequiredMixin, views.DeleteView):
    model = ServiceOrderNote
    template_name = 'service_order_note/service_order_note_delete.html'

    def get_success_url(self):
        go_to_next = self.request.POST.get('next', '/')
        return go_to_next


def rollback_service_order(request, pk):
    service_order_header = ServiceOrderHeader.objects.get(pk=pk)
    service_order_header.is_serviced = False
    service_order_header.serviced_by = None
    service_order_header.serviced_on = None
    service_order_header.save()

    return redirect('service_orders_list_pending_service')


class HandoverServiceOrderView(auth_mixins.LoginRequiredMixin, views.UpdateView):
    model = ServiceOrderHeader
    form_class = HandoverServiceOrderForm
    template_name = 'service_order_header/core/service_order_handover.html'
    success_url = reverse_lazy('service_orders_list_serviced')

    def get_initial(self):
        service_order_header_id = self.kwargs['pk']

        if service_order_header_id:
            self.initial.update({
                'service_order': service_order_header_id,
            })

        return super().get_initial()

    def form_valid(self, form):
        service_order_header_id = self.kwargs['pk']
        service_order_header = ServiceOrderHeader.objects.filter(pk=service_order_header_id).get()
        service_order_header.is_completed = True
        service_order_header.completed_by = self.request.user
        service_order_header.completed_on = datetime.datetime.now()
        service_order_header.save()

        return redirect('service_orders_list_pending_service')
