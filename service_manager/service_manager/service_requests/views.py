from django.contrib.auth.decorators import permission_required
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth import mixins as auth_mixins
import django.views.generic as views
from django.urls import reverse_lazy, reverse

from service_manager.core.mixins import MaterialFilteringMixin
from service_manager.core.utils import get_material_count_matching_conditions
from service_manager.customers.models import CustomerAsset, Customer
from service_manager.customers.utils import get_assets_currently_in_service
from service_manager.main.forms import ServiceRequestFilteringForm, CreateServiceRequestForm, \
    ServiceRequestAssignHandlerForm, ServiceRequestUpdateResolutionForm
from service_manager.main.models import ServiceRequest
import datetime as dt
from dateutil import relativedelta
import datetime

from service_manager.master_data.forms import FilterMaterialForm
from service_manager.master_data.models import Material
from service_manager.service_requests.forms import CreateDeliveryRequestForm, EditDeliveryRequestForm
from service_manager.service_requests.models import DeliveryRequest


# Create your views here.
class ServiceRequestsListView(auth_mixins.PermissionRequiredMixin, views.ListView):
    model = ServiceRequest
    template_name = 'service_request/service_requests.html'

    permission_required = 'main.view_serviceorderheader'

    paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        today = dt.datetime.now().date()

        if 'search' in self.request.GET:
            search_text = self.request.GET['search']
            queryset = queryset.filter(
                Q(customer__name__icontains=search_text) | Q(problem_description__icontains=search_text))

        if 'status' in self.request.GET:
            status = self.request.GET.getlist('status')

            queryset = queryset.filter(status__in=[int(x) for x in status])

        if 'period' in self.request.GET:
            period = self.request.GET.getlist('period')
            conditions = []
            combined_conditions = Q()

            if '0' in period:
                start = today
                end = today + dt.timedelta(days=1)
                conditions.append((start, end))

            if '1' in period:
                start = today - dt.timedelta(days=today.weekday())
                end = start + dt.timedelta(days=7)
                conditions.append((start, end))

            if '2' in period:
                start = today - dt.timedelta(days=(today.weekday() + 7))
                end = start + dt.timedelta(days=7)
                conditions.append((start, end))

            if '3' in period:
                start = today.replace(day=1)
                end = today + relativedelta.relativedelta(months=1, day=1)
                conditions.append((start, end))

            if '4' in period:
                start = today - relativedelta.relativedelta(months=1, day=1)
                end = today.replace(day=1)
                conditions.append((start, end))

            if '5' in period:
                end = today - relativedelta.relativedelta(months=1, day=1)
                conditions.append(end)

            for x in conditions:
                if isinstance(x, tuple):
                    condition = Q(created_on__range=(x[0], x[1]))
                else:
                    condition = Q(created_on__lte=x)
                combined_conditions |= condition

            queryset = queryset.filter(combined_conditions)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        queryset = self.get_queryset()
        open_service_requests_cnt = queryset.filter(status__in=['1', '2', '3']).count()

        request = self.request.GET.copy()
        params = request.pop('page', True) and request.urlencode()
        context['params'] = params

        context['open_service_requests_cnt'] = open_service_requests_cnt
        context['filter_form'] = ServiceRequestFilteringForm(self.request.GET or None)
        return context


class ServiceRequestDetailView(auth_mixins.PermissionRequiredMixin, views.DetailView):
    model = ServiceRequest
    template_name = 'service_request/service_request_detail.html'
    context_object_name = 'service_request'

    permission_required = 'main.view_serviceorderheader'


class CreateServiceRequestView(auth_mixins.PermissionRequiredMixin, views.CreateView):
    model = ServiceRequest
    template_name = 'service_request/create_service_request.html'
    form_class = CreateServiceRequestForm

    permission_required = 'main.add_serviceorderheader'

    def form_valid(self, form):
        service_request = form.save(commit=False)
        service_request.accepted_by = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        go_to_next = reverse_lazy('service_requests')
        return go_to_next + '?period=1&status=1&status=2&status=3'


class EditServiceRequestView(auth_mixins.PermissionRequiredMixin, views.UpdateView):
    model = ServiceRequest
    template_name = 'service_request/edit_service_request.html'
    form_class = CreateServiceRequestForm

    permission_required = 'main.change_serviceorderheader'

    def get_success_url(self):
        service_request = ServiceRequest.objects.all().get(pk=self.kwargs['pk'])
        # Delivery
        if service_request.order_type == 2:
            return reverse_lazy('create_delivery_request', kwargs={'service_request_id': self.kwargs['pk']})
        # Service
        return reverse_lazy('service_request_detail', kwargs={'pk': self.kwargs['pk']})



class ServiceRequestAssignHandlerView(EditServiceRequestView):
    form_class = ServiceRequestAssignHandlerForm
    template_name = 'service_request/service_request_assign_handler.html'

    def form_valid(self, form):
        service_request = form.save(commit=False)
        service_request.handled_on = datetime.datetime.now()
        service_request.status = ServiceRequest.TYPE_IN_PROGRESS
        service_request.save()

        return super().form_valid(form)


class ServiceRequestUpdateResolutionView(EditServiceRequestView):
    form_class = ServiceRequestUpdateResolutionForm
    template_name = 'service_request/service_request_update_resolution.html'

    def form_valid(self, form):
        service_request = form.save(commit=False)
        service_request.status = ServiceRequest.TYPE_RESOLVED
        service_request.save()

        return super().form_valid(form)


class DeleteServiceRequestView(auth_mixins.PermissionRequiredMixin, views.DeleteView):
    model = ServiceRequest
    template_name = 'service_request/delete_service_request.html'

    permission_required = 'main.delete_serviceorderheader'

    def get_success_url(self):
        success_url = reverse('service_requests') + '?period=1'

        return success_url


@permission_required('main.change_serviceorderheader')
def finalize_service_request(request, pk):
    service_request = ServiceRequest.objects.get(pk=pk)
    service_request.status = ServiceRequest.TYPE_CLOSED
    service_request.closed_on = datetime.datetime.now()
    service_request.closed_by = request.user
    service_request.save()

    return redirect(reverse_lazy('service_request_detail', kwargs={'pk': pk}))


@permission_required('main.change_serviceorderheader')
def reject_service_request(request, pk):
    service_request = ServiceRequest.objects.get(pk=pk)
    service_request.status = ServiceRequest.TYPE_REJECTED
    service_request.closed_on = datetime.datetime.now()
    service_request.closed_by = request.user
    service_request.save()

    return redirect(reverse_lazy('service_request_detail', kwargs={'pk': pk}))


class ServiceRequestCreateServiceOrder(auth_mixins.PermissionRequiredMixin, views.ListView):
    model = CustomerAsset
    template_name = 'customer_asset/customer_assets_list.html'
    # permission_required = 'customers.add_customerasset'

    context_object_name = 'customer_assets'

    permission_required = 'main.add_serviceorderheader'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(customer__pk=self.kwargs['customer_id'])

        search_text = self.request.GET.get('search_value', None)
        if search_text:
            queryset = queryset.filter(
                Q(asset__category__name__icontains=search_text) |
                Q(asset__brand__name__icontains=search_text) |
                Q(asset__model_number__icontains=search_text) |
                Q(asset__model_name__icontains=search_text) |
                Q(serial_number__icontains=search_text)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = Customer.objects.get(pk=self.kwargs['customer_id'])

        context['service_request_id'] = self.kwargs['pk']
        context['assets_being_serviced'] = get_assets_currently_in_service(customer)
        context['customer'] = customer
        return context


class CreateDeliveryRequestView(MaterialFilteringMixin, auth_mixins.PermissionRequiredMixin, views.CreateView):
    model = DeliveryRequest
    template_name = 'delivery_request/delivery_request_create.html'
    permission_required = 'main.add_serviceorderheader'
    form_class = CreateDeliveryRequestForm

    context_object_name = 'delivery_request'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        service_request = ServiceRequest.objects.all().get(pk=self.kwargs['service_request_id'])
        context['service_request'] = service_request

        context['filter_form'] = FilterMaterialForm(self.request.GET or None)

        context['material_count'] = get_material_count_matching_conditions(
            self.request.GET.get('category' or None),
            self.request.GET.get('search' or None)
        )

        return context

    def get_success_url(self):
        return reverse_lazy('create_delivery_request', kwargs={'service_request_id': self.kwargs['service_request_id']})

    def form_valid(self, form):
        service_request_id = self.kwargs['service_request_id']
        service_request = ServiceRequest.objects.all().get(pk=service_request_id)

        delivery_request = form.save(commit=False)
        delivery_request.service_request = service_request
        delivery_request.save()

        return super().form_valid(form)


class EditDeliveryRequestView(auth_mixins.PermissionRequiredMixin, views.UpdateView):
    model = DeliveryRequest
    template_name = 'delivery_request/delivery_request_edit.html'
    permission_required = 'main.change_serviceorderheader'

    form_class = EditDeliveryRequestForm

    def get_success_url(self):
        return reverse_lazy('create_delivery_request', kwargs={'service_request_id': self.kwargs['service_request_id']})


class DeleteDeliveryRequestView(auth_mixins.PermissionRequiredMixin, views.DeleteView):
    model = DeliveryRequest
    template_name = 'delivery_request/delivery_request_delete.html'
    permission_required = 'main.change_serviceorderheader'

    def get_success_url(self):
        return reverse_lazy('create_delivery_request', kwargs={'service_request_id': self.kwargs['service_request_id']})

# class DeliveryRequestListView(auth_mixins.PermissionRequiredMixin, views.ListView):
#     model = DeliveryRequest
#     template_name = ''
#     permission_required = 'main.add_serviceorderheader'
#
#     context_object_name = 'delivery_requests'

