from django.contrib import admin

from service_manager.master_data.models import CustomerType, Asset, AssetCategory, Brand, Material, MaterialCategory


@admin.register(CustomerType)
class CustomerTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ['brand', 'model_number', 'model_name', 'category']


@admin.register(AssetCategory)
class AssetCategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    pass


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price']


@admin.register(MaterialCategory)
class MaterialCategoryAdmin(admin.ModelAdmin):
    pass
