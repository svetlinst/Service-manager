from rest_framework import serializers
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