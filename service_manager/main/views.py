from django.http import HttpResponse
from django.shortcuts import render
import django.views.generic as views

from service_manager.main.models import Customer


def get_index(request):
    return render(request, 'index.html')


class CustomersListView(views.ListView):
    model = Customer
    template_name = 'customers.html'
    ordering = ('name',)


class CustomerUpdateView(views.UpdateView):
    model = Customer
    fields = '__all__'
    template_name = 'customer_details.html'
