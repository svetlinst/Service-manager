from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets

from service_manager.api.serializers import CustomerSerializer
from service_manager.customers.models import Customer


# Create your views here.
class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()
