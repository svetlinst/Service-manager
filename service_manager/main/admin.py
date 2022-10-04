from django.contrib import admin

from service_manager.main.models import ServiceOrderHeader, ServiceOrderDetail


@admin.register(ServiceOrderHeader)
class ServiceOrderHeaderAdmin(admin.ModelAdmin):
    list_display = ['customer', 'customer_asset', 'department', 'is_completed']


@admin.register(ServiceOrderDetail)
class ServiceOrderDetailAdmin(admin.ModelAdmin):
    list_display = ['service_order', 'material', 'quantity', 'discount']
