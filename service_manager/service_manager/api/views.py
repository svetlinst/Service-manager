from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response

from service_manager.api.serializers import CustomerSerializer, ServiceRequestSerializer
from service_manager.customers.models import Customer
from service_manager.main.models import ServiceRequest


# Create your views here.
class CustomerViewSet(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()


class ServiceRequestViewSet(viewsets.ModelViewSet):
    serializer_class =ServiceRequestSerializer
    queryset = ServiceRequest.objects.all()

class CustomerNamesViewSet(viewsets.ViewSet):
    def list(self, request):
        customers = Customer.objects.all()
        data = [{'id': customer.id, 'name': customer.name} for customer in customers]
        return Response(data)