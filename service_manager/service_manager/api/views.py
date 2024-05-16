from django.http import Http404
from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response

from service_manager.accounts.models import Profile, AppUser
from service_manager.api.serializers import CustomerSerializer, ServiceRequestSerializer, AppUserSerializer
from service_manager.customers.models import Customer
from service_manager.main.models import ServiceRequest


# Create your views here.
class CustomerViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()


class ServiceRequestViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class =ServiceRequestSerializer
    queryset = ServiceRequest.objects.all()

class CustomerNamesViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]
    def list(self, request):
        customers = Customer.objects.all()
        data = [{'id': customer.id, 'name': customer.name} for customer in customers]
        return Response(data)


class UserDetailApiView(APIView):
    def get_object(self, email):
        try:
            return AppUser.objects.get(email=email)
        except AppUser.DoesNotExist:
            raise Http404

    def get(self, request, email):
        app_user = self.get_object(email)
        serializer = AppUserSerializer(app_user)
        return Response(serializer.data)
