import datetime

from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
import django.views.generic as views
from django.urls import reverse_lazy
from django.db.models import Q

from service_manager.main.forms import EditCustomerForm, CreateCustomerForm, CreateAssetForm, EditAssetForm, \
    CreateMaterialForm, EditMaterialForm, CreateCustomerAssetForm, EditCustomerAssetForm, CreateServiceOrderHeaderForm, \
    EditCustomerRepresentativeForm, CreateCustomerRepresentativeForm, CreateServiceOrderDetailForm, \
    EditServiceOrderDetailForm, CreateCustomerDepartmentForm, CreateServiceOrderNoteForm
from service_manager.main.models import Customer, Asset, Material, CustomerAsset, ServiceOrderHeader, \
    CustomerRepresentative, ServiceOrderDetail, CustomerDepartment, ServiceOrderNote


def get_index(request):
    return render(request, 'index.html')


class CustomersListView(views.ListView):
    model = Customer
    template_name = 'customer/customers.html'
    ordering = ('name',)

    def get_queryset(self):
        queryset = super().get_queryset()

        search_text = self.request.GET.get('search_value', None)
        if search_text:
            queryset = queryset.filter(Q(name__icontains=search_text) | Q(vat__icontains=search_text))
        return queryset


class EditCustomerView(views.UpdateView):
    model = Customer
    form_class = EditCustomerForm
    template_name = 'customer/customer_edit.html'
    success_url = reverse_lazy('customers_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = context['customer']

        context['customer_assets'] = customer.customerasset_set.all()
        context['customer_representatives'] = customer.customerrepresentative_set.all()
        context['customer_departments'] = customer.customerdepartment_set.all()

        search_text = self.request.GET.get('search_value', None)
        if search_text:
            context['customer_assets'] = customer.customerasset_set.filter(serial_number__icontains=search_text)

        representative_search = self.request.GET.get('representative', None)
        if representative_search:
            context['customer_representatives'] = customer.customerrepresentative_set.filter(
                Q(first_name__icontains=representative_search) | Q(last_name__icontains=representative_search))

        department_search = self.request.GET.get('departments', None)
        if department_search:
            context['customer_departments'] = customer.customerdepartment_set.filter(name__icontains=department_search)

        return context


class CreateCustomerView(views.CreateView):
    model = Customer
    form_class = CreateCustomerForm
    template_name = 'customer/customer_create.html'
    success_url = reverse_lazy('customers_list')


class DeleteCustomerView(views.DeleteView):
    model = Customer
    template_name = 'customer/customer_delete.html'
    success_url = reverse_lazy('customers_list')


class AssetsListView(views.ListView):
    model = Asset
    template_name = 'asset/assets.html'
    ordering = ('category', 'brand', 'model_name', 'model_number')


class CreateAssetView(views.CreateView):
    model = Asset
    form_class = CreateAssetForm
    template_name = 'asset/asset_create.html'
    success_url = reverse_lazy('assets_list')


class EditAssetView(views.UpdateView):
    model = Asset
    form_class = EditAssetForm
    template_name = 'asset/asset_edit.html'
    success_url = reverse_lazy('assets_list')


class DeleteAssetView(views.DeleteView):
    model = Asset
    template_name = 'asset/asset_delete.html'
    success_url = reverse_lazy('assets_list')


class MaterialsListView(views.ListView):
    model = Material
    template_name = 'material/materials.html'
    ordering = ('category', 'name')


class CreateMaterialView(views.CreateView):
    model = Material
    form_class = CreateMaterialForm
    template_name = 'material/material_create.html'
    success_url = reverse_lazy('materials_list')


class EditMaterialView(views.UpdateView):
    model = Material
    form_class = EditMaterialForm
    template_name = 'material/material_edit.html'
    success_url = reverse_lazy('materials_list')


class DeleteMaterialView(views.DeleteView):
    model = Material
    template_name = 'material/material_delete.html'
    success_url = reverse_lazy('materials_list')


class CreateCustomerAssetView(views.CreateView):
    model = CustomerAsset
    form_class = CreateCustomerAssetForm
    template_name = 'customer_asset/customer_asset_create.html'

    def get_success_url(self):
        return reverse_lazy('edit_customer', kwargs={'pk': self.object.customer.pk})

    def get_initial(self):
        customer_id = self.kwargs['customer_id']
        if customer_id:
            self.initial.update({
                'customer': customer_id,
            })
        return super().get_initial()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        customer_id = self.kwargs['customer_id']
        if customer_id:
            customer = Customer.objects.prefetch_related('customerasset_set').filter(pk=customer_id).get()
            context['customer'] = customer
        return context


class EditCustomerAssetView(views.UpdateView):
    model = CustomerAsset
    form_class = EditCustomerAssetForm
    template_name = 'customer_asset/customer_asset_edit.html'

    def get_success_url(self):
        return reverse_lazy('edit_customer', kwargs={'pk': self.object.customer.pk})


class DeleteCustomerAssetView(views.DeleteView):
    model = CustomerAsset
    template_name = 'customer_asset/customer_asset_delete.html'

    def get_success_url(self):
        return reverse_lazy('edit_customer', kwargs={'pk': self.object.customer.pk})


class ServiceOrderHeaderListView(views.ListView):
    model = ServiceOrderHeader
    template_name = 'service_order_header/service_orders.html'
    ordering = ('created_on', 'customer')

    def get_queryset(self):
        return ServiceOrderHeader.objects.filter(is_serviced=False).prefetch_related('serviceordernote_set')


class ServiceOrderHeaderDetailView(views.DetailView):
    model = ServiceOrderHeader
    template_name = 'service_order_header/service_order_details.html'
    context_object_name = 'service_order_header'


class CreateServiceOrderHeader(views.CreateView):
    model = ServiceOrderHeader
    form_class = CreateServiceOrderHeaderForm
    template_name = 'service_order_header/service_order_create.html'

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


class DeleteServiceOrderHeaderView(views.DeleteView):
    model = ServiceOrderHeader
    template_name = 'service_order_header/service_order_delete.html'
    success_url = reverse_lazy('service_orders_list')


def load_customer_representatives(request):
    customer = request.GET.get('customer', None)
    if customer:
        customer_representatives = CustomerRepresentative.objects.filter(customer=customer)
        context = {
            'customer_representatives': customer_representatives,
        }
        return render(request, 'partial/customer_representatives.html', context)


class CustomerRepresentativesListView(views.ListView):
    model = CustomerRepresentative
    template_name = 'customer_representatives/customer_representatives.html'
    ordering = ('first_name', 'last_name')


class CreateCustomerRepresentativeView(views.CreateView):
    model = CustomerRepresentative
    template_name = 'customer_representatives/customer_representatives_create.html'
    form_class = CreateCustomerRepresentativeForm

    def get_initial(self):
        customer_id = self.kwargs['customer_id']
        if customer_id:
            self.initial.update({
                'customer': customer_id,
            })
        return super().get_initial()

    def get_success_url(self):
        return reverse_lazy('edit_customer', kwargs={'pk': self.object.customer.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        customer_id = self.kwargs['customer_id']
        if customer_id:
            customer = Customer.objects.prefetch_related('customerrepresentative_set').filter(pk=customer_id).get()
            context['customer'] = customer
        return context


class EditCustomerRepresentativeView(views.UpdateView):
    model = CustomerRepresentative
    template_name = 'customer_representatives/customer_representative_edit.html'
    form_class = EditCustomerRepresentativeForm

    def get_success_url(self):
        return reverse_lazy('edit_customer', kwargs={'pk': self.object.customer.pk})


class DeleteCustomerRepresentativeView(views.DeleteView):
    model = CustomerRepresentative
    template_name = 'customer_representatives/customer_representative_delete.html'

    def get_success_url(self):
        return reverse_lazy('edit_customer', kwargs={'pk': self.object.customer.pk})


class CreateServiceOrderDetailView(views.CreateView):
    model = ServiceOrderDetail
    template_name = 'service_order_detail/service_order_details_create.html'
    form_class = CreateServiceOrderDetailForm

    def get_initial(self):
        service_order_id = self.kwargs['order_id']

        if service_order_id:
            self.initial.update({
                'service_order': service_order_id,
            })

        return super().get_initial()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        service_order_header_id = self.kwargs['order_id']
        if service_order_header_id:
            context['service_order_header'] = ServiceOrderHeader.objects.prefetch_related(
                'serviceorderdetail_set').filter(pk=int(service_order_header_id)).get()

        return context

    def get_success_url(self):
        service_order_header_id = self.kwargs['order_id']
        if service_order_header_id:
            return reverse_lazy('create_service_order_detail', kwargs={'order_id': service_order_header_id})
        return reverse_lazy('service_orders_list')


class EditServiceOrderDetailView(views.UpdateView):
    model = ServiceOrderDetail
    template_name = 'service_order_detail/service_order_detail_edit.html'
    form_class = EditServiceOrderDetailForm

    def get_success_url(self):
        service_order_header_id = self.kwargs['order_id']
        if service_order_header_id:
            return reverse_lazy('create_service_order_detail', kwargs={'order_id': service_order_header_id})
        return reverse_lazy('service_orders_list')


class ServiceOrderDetailsListView(views.ListView):
    model = ServiceOrderDetail
    template_name = 'service_order_detail/service_order_details.html'
    ordering = ('material', 'quantity',)


class DeleteServiceOrderDetailView(views.DeleteView):
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
    service_order_header.serviced_by = request.user.employee
    service_order_header.serviced_on = datetime.datetime.now()
    service_order_header.save()

    return redirect('service_orders_list')


class CustomerDepartmentsListView(views.ListView):
    model = CustomerDepartment
    template_name = 'customer_department/customer_departments.html'


class CreateCustomerDepartmentView(views.CreateView):
    model = CustomerDepartment
    template_name = 'customer_department/customer_department_create.html'
    form_class = CreateCustomerDepartmentForm

    def get_initial(self):
        customer_id = self.kwargs['customer_id']

        if customer_id:
            self.initial.update({
                'customer': customer_id,
            })

        return super().get_initial()

    def get_success_url(self):
        customer_id = self.kwargs['customer_id']
        if customer_id:
            return reverse_lazy('edit_customer', kwargs={'pk': customer_id})
        return reverse_lazy('customers_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        customer_id = self.kwargs['customer_id']
        if customer_id:
            customer = Customer.objects.prefetch_related('customerdepartment_set').filter(pk=customer_id).get()
            context['customer'] = customer
        return context


class EditCustomerDepartmentView(views.UpdateView):
    model = CustomerDepartment
    template_name = 'customer_department/customer_department_edit.html'
    form_class = CreateCustomerDepartmentForm

    def get_success_url(self):
        customer_id = self.kwargs['customer_id']
        if customer_id:
            return reverse_lazy('edit_customer', kwargs={'pk': customer_id})
        return reverse_lazy('customers_list')


class DeleteCustomerDepartmentView(views.DeleteView):
    model = CustomerDepartment
    template_name = 'customer_department/customer_department_delete.html'

    def get_success_url(self):
        customer_id = self.kwargs['customer_id']
        if customer_id:
            return reverse_lazy('edit_customer', kwargs={'pk': customer_id})
        return reverse_lazy('customers_list')


class CreateServiceOrderNoteView(views.CreateView):
    model = ServiceOrderNote
    template_name = 'service_order_note_create.html'
    form_class = CreateServiceOrderNoteForm

    def get_initial(self):
        # todo: Add the user as created by
        user = self.request.user

        service_order_header_id = self.kwargs['order_id']

        if service_order_header_id:
            self.initial.update({
                'service_order': service_order_header_id,
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


class ServiceOrderNotesListView(views.ListView):
    model = ServiceOrderNote
    template_name = 'service_order_notes.html'


class EditServiceOrderNoteView(views.UpdateView):
    pass


class DeleteServiceOrderNoteView(views.DeleteView):
    pass
