from django.contrib import admin

from service_manager.customers.models import Customer, CustomerRepresentative, CustomerDepartment, CustomerAsset


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'vat', 'type', 'email_address', 'phone_number']


@admin.register(CustomerRepresentative)
class CustomerRepresentativeAdmin(admin.ModelAdmin):
    list_display = ['customer', 'first_name', 'last_name', 'email_address', 'phone_number']


@admin.register(CustomerDepartment)
class CustomerDepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'customer']


@admin.register(CustomerAsset)
class CustomerAssetAdmin(admin.ModelAdmin):
    list_display = ['customer', 'asset', 'serial_number', 'product_number']
