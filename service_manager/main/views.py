from django.http import HttpResponse
from django.shortcuts import render
import django.views.generic as views
from django.urls import reverse_lazy

from service_manager.main.forms import EditCustomerForm, CreateCustomerForm
from service_manager.main.models import Customer, Asset


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


# class AssetsListView(views.ListView):
#     model = Asset
#     ordering = ('model_name', 'model_number')

