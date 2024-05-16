from rest_framework import serializers

from service_manager.accounts.models import Profile, AppUser
from service_manager.customers.models import Customer
from service_manager.main.models import ServiceRequest


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class ServiceRequestSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all()
    )

    class Meta:
        model = ServiceRequest
        fields = '__all__'

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class AppUserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    class Meta:
        model = AppUser
        fields = ['profile', 'email', 'is_active', 'is_staff', 'is_superuser']