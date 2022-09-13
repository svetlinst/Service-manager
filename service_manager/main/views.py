from django.http import HttpResponse
from django.shortcuts import render
import django.views.generic as views
from django.urls import reverse_lazy

from service_manager.main.forms import EditCustomerForm, CreateCustomerForm, CreateAssetForm, EditAssetForm, \
    CreateMaterialForm, EditMaterialForm
from service_manager.main.models import Customer, Asset, Material


def get_index(request):
    return render(request, 'index.html')


class CustomersListView(views.ListView):
    model = Customer
    template_name = 'customers.html'
    ordering = ('name',)


class EditCustomerView(views.UpdateView):
    model = Customer
    form_class = EditCustomerForm
    template_name = 'customer_edit.html'
    success_url = reverse_lazy('customers_list')


class CreateCustomerView(views.CreateView):
    model = Customer
    form_class = CreateCustomerForm
    template_name = 'customer_create.html'
    success_url = reverse_lazy('customers_list')


class DeleteCustomerView(views.DeleteView):
    model = Customer
    template_name = 'customer_delete.html'
    success_url = reverse_lazy('customers_list')


class AssetsListView(views.ListView):
    model = Asset
    template_name = 'assets.html'
    ordering = ('model_name', 'model_number')


class CreateAssetView(views.CreateView):
    model = Asset
    form_class = CreateAssetForm
    template_name = 'asset_create.html'
    success_url = reverse_lazy('assets_list')


class EditAssetView(views.UpdateView):
    model = Asset
    form_class = EditAssetForm
    template_name = 'asset_edit.html'
    success_url = reverse_lazy('assets_list')


class DeleteAssetView(views.DeleteView):
    model = Asset
    template_name = 'asset_delete.html'
    success_url = reverse_lazy('assets_list')


class MaterialsListView(views.ListView):
    model = Material
    template_name = 'materials.html'
    ordering = ('name', 'category')


class CreateMaterialView(views.CreateView):
    model = Material
    form_class = CreateMaterialForm
    template_name = 'material_create.html'
    success_url = reverse_lazy('materials_list')


class EditMaterialView(views.UpdateView):
    model = Material
    form_class = EditMaterialForm
    template_name = 'material_edit.html'
    success_url = reverse_lazy('materials_list')


class DeleteMaterialView(views.DeleteView):
    model = Material
    template_name = 'material_delete.html'
    success_url = reverse_lazy('materials_list')
