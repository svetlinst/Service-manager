from rest_framework import serializers

from service_manager.main.models import ServiceOrderHeader


class ServiceOrderHeaderSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceOrderHeader
        fields = '__all__'
