from django.contrib.auth.decorators import permission_required
from django.db.models import Q
from django.shortcuts import render, redirect
from django.contrib.auth import mixins as auth_mixins
import django.views.generic as views
from django.urls import reverse_lazy, reverse

from service_manager.customers.models import CustomerAsset, Customer
from service_manager.customers.utils import get_assets_currently_in_service
from service_manager.main.forms import ServiceRequestFilteringForm, CreateServiceRequestForm, \
    ServiceRequestAssignHandlerForm, ServiceRequestUpdateResolutionForm
from service_manager.main.models import ServiceRequest
import datetime as dt
from dateutil import relativedelta
import datetime


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
            queryset = queryset.filter(customer__name__icontains=search_text)

        if 'status' in self.request.GET:
            status = self.request.GET['status']

            if status != '0':
                queryset = queryset.filter(status=int(status))

        if 'period' in self.request.GET:
            period = self.request.GET['period']

            # today
            if period == '0':
                start = today
                end = today + dt.timedelta(days=1)
                queryset = queryset.filter(created_on__range=(
                    start,
                    end)
                )

            # this week
            if period == '1':
                start = today - dt.timedelta(days=today.weekday())
                end = start + dt.timedelta(days=7)
                queryset = queryset.filter(created_on__range=(
                    start,
                    end)
                )

            # last week
            if period == '2':
                start = today - dt.timedelta(days=(today.weekday() + 7))
                end = start + dt.timedelta(days=7)
                queryset = queryset.filter(created_on__range=(
                    start,
                    end)
                )

            # this month
            if period == '3':
                start = today.replace(day=1)
                end = today + relativedelta.relativedelta(months=1, day=1)
                queryset = queryset.filter(created_on__range=(
                    start,
                    end)
                )

            # last month
            if period == '4':
                start = today - relativedelta.relativedelta(months=1, day=1)
                end = today.replace(day=1)
                queryset = queryset.filter(created_on__range=(
                    start,
                    end)
                )

            # older
            if period == '5':
                end = today - relativedelta.relativedelta(months=1, day=1)
                queryset = queryset.filter(created_on__lte=end)

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
        go_to_next = self.request.POST.get('next', '/')
        return go_to_next + '?period=1'


class EditServiceRequestView(auth_mixins.PermissionRequiredMixin, views.UpdateView):
    model = ServiceRequest
    template_name = 'service_request/edit_service_request.html'
    form_class = CreateServiceRequestForm

    permission_required = 'main.change_serviceorderheader'

    def get_success_url(self):
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
