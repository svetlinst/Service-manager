from django.contrib import admin

from service_manager.accounts.models import Profile, AppUser
from service_manager.main.models import Customer, CustomerType, CustomerRepresentative, CustomerDepartment, Asset, \
    CustomerAsset, Material, ServiceOrderHeader, \
    ServiceOrderDetail
from service_manager.master_data.models import AssetCategory, Brand, MaterialCategory


@admin.register(AppUser)
class AppUserAdmin(admin.ModelAdmin):
    pass


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'vat', 'type', 'email_address', 'phone_number']


@admin.register(CustomerType)
class CustomerTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(CustomerRepresentative)
class CustomerRepresentativeAdmin(admin.ModelAdmin):
    list_display = ['customer', 'first_name', 'last_name', 'email_address', 'phone_number']


@admin.register(CustomerDepartment)
class CustomerDepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'customer']


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ['brand', 'model_number', 'model_name', 'category']


@admin.register(AssetCategory)
class AssetCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    pass


@admin.register(CustomerAsset)
class CustomerAssetAdmin(admin.ModelAdmin):
    list_display = ['customer', 'asset', 'serial_number', 'product_number']


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['first_name']


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price']


@admin.register(MaterialCategory)
class MaterialCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(ServiceOrderHeader)
class ServiceOrderHeaderAdmin(admin.ModelAdmin):
    list_display = ['customer', 'customer_asset', 'department', 'is_completed']


@admin.register(ServiceOrderDetail)
class ServiceOrderDetailAdmin(admin.ModelAdmin):
    list_display = ['service_order', 'material', 'quantity', 'discount']
