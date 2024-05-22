from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from service_manager.accounts.models import Profile, AppUser
from service_manager.api.serializers import CustomerSerializer, ServiceRequestSerializer, AppUserSerializer, \
    ProfileSerializer
from service_manager.customers.models import Customer
from service_manager.main.models import ServiceRequest


# Create your views here.
class CustomerViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()


class ServiceRequestViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ServiceRequestSerializer
    queryset = ServiceRequest.objects.all()


class CustomerNamesViewSet(viewsets.ViewSet):
    permission_classes = [IsAuthenticated]

    def list(self, request):
        customers = Customer.objects.all()
        data = [{'id': customer.id, 'name': customer.name} for customer in customers]
        return Response(data)


class UserDetailApiView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, email):
        app_user = get_object_or_404(AppUser, email=email)
        serializer = AppUserSerializer(app_user)
        return Response(serializer.data)


class ProfileViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

    def get_object(self):
        queryset = self.get_queryset()
        filter_kwargs = {'app_user_id': self.kwargs.get('id', None)}
        profile = get_object_or_404(queryset, **filter_kwargs)
        self.check_object_permissions(self.request, profile)
        return profile
