from django.http import HttpResponse
from django.shortcuts import render
import django.views.generic as views
from django.urls import reverse_lazy

from service_manager.main.forms import EditCustomerForm, CreateCustomerForm, CreateAssetForm, EditAssetForm, \
    CreateMaterialForm, EditMaterialForm, CreateCustomerAssetForm, EditCustomerAssetForm, CreateServiceOrderHeaderForm
from service_manager.main.models import Customer, Asset, Material, CustomerAsset, ServiceOrderHeader, \
    CustomerRepresentative


def get_index(request):
    return render(request, 'index.html')


class CustomersListView(views.ListView):
    model = Customer
    template_name = 'customer/customers.html'
    ordering = ('name',)


class EditCustomerView(views.UpdateView):
    model = Customer
    form_class = EditCustomerForm
    template_name = 'customer/customer_edit.html'
    success_url = reverse_lazy('customers_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = context['customer']

        context['customer_assets'] = customer.customerasset_set.all()

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
    ordering = ('model_name', 'model_number')


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
    ordering = ('name', 'category')


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
    success_url = reverse_lazy('customers_list')

    def get_initial(self):
        initial = {}
        customer_id = self.request.GET.get('customer_id', None)
        if customer_id:
            initial['customer'] = customer_id
        return initial

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #
    #     filter = self.request.GET.get('customer_id', None)
    #
    #     if filter:
    #         queryset = queryset.filter(customer_id=filter)
    #
    #     return queryset


class EditCustomerAssetView(views.UpdateView):
    model = CustomerAsset
    form_class = EditCustomerAssetForm
    template_name = 'customer_asset/customer_asset_edit.html'
    success_url = reverse_lazy('customers_list')


class DeleteCustomerAssetView(views.DeleteView):
    model = CustomerAsset
    template_name = 'customer_asset/customer_asset_delete.html'
    success_url = reverse_lazy('customers_list')


class ServiceOrderHeaderListView(views.ListView):
    model = ServiceOrderHeader
    template_name = 'service_orders.html'
    ordering = ('-created_on', 'customer')


class ServiceOrderHeaderDetailView(views.DetailView):
    model = ServiceOrderHeader
    template_name = 'service_order_details.html'


class CreateServiceOrderHeader(views.CreateView):
    model = ServiceOrderHeader
    form_class = CreateServiceOrderHeaderForm
    template_name = 'service_order_create.html'
    success_url = reverse_lazy('customers_list')

    # def get_initial(self):
    #     initial = {}
    #     customer_id = self.request.GET.get('customer_id', None)
    #     if customer_id:
    #         initial['customer'] = customer_id
    #     return initial

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #
    #     filter = self.request.GET.get('customer_id', None)
    #
    #     if filter:
    #         queryset = queryset.filter(customer_id=filter)
    #
    #     return queryset
    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     customer = context['customer']
    #
    #     context['customer_representatives'] = customer.customerrepresentative_set.all()
    #     context['customer_assets'] = customer.customerasset_set.all()
    #
    #     return context


def load_customer_representatives(request):
    customer = request.GET.get('customer', None)

    if customer:
        customer_representatives = CustomerRepresentative.objects.filter(customer=customer)

        context = {
            'customer_representatives': customer_representatives,
        }

        return render(request, 'customer_representatives.html', context)
