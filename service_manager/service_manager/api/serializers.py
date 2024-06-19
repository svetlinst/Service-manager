from rest_framework import serializers

from service_manager.accounts.models import Profile, AppUser
from service_manager.customers.models import Customer
from service_manager.main.models import ServiceRequest


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Customer
        fields = '__all__'


class ServiceRequestInputSerializer(serializers.ModelSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    status_display = serializers.SerializerMethodField()

    def get_status_display(self, obj):
        return obj.get_status_display()

    class Meta:
        model = ServiceRequest
        fields = '__all__'


class ServiceRequestOutputSerializer(ServiceRequestInputSerializer):
    customer = CustomerSerializer()


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'phone_number']


class AppUserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = AppUser
        fields = ['profile', 'email', 'is_active', 'is_staff', 'is_superuser', 'id', 'is_customer', 'customer_id']
