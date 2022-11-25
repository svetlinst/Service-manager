import django.views.generic as views
from django.urls import reverse_lazy
from django.contrib.auth import mixins as auth_mixins

from service_manager.core.views import BootstrapFormViewMixin
from service_manager.master_data.forms import CreateAssetForm, EditAssetForm, CreateMaterialForm, EditMaterialForm, \
    EditMaterialCategoryForm, EditBrandForm, EditAssetCategoryForm
from service_manager.master_data.models import Asset, Material, MaterialCategory, Brand, AssetCategory


class AssetsListView(auth_mixins.PermissionRequiredMixin, views.ListView):
    model = Asset
    template_name = 'asset/assets.html'
    ordering = ('category', 'brand', 'model_name', 'model_number')

    permission_required = 'master_data.view_asset'


class CreateAssetView(auth_mixins.PermissionRequiredMixin, views.CreateView):
    model = Asset
    form_class = CreateAssetForm
    template_name = 'asset/asset_create.html'
    success_url = reverse_lazy('assets_list')

    permission_required = 'master_data.add_asset'


class EditAssetView(auth_mixins.PermissionRequiredMixin, views.UpdateView):
    model = Asset
    form_class = EditAssetForm
    template_name = 'asset/asset_edit.html'
    success_url = reverse_lazy('assets_list')

    permission_required = 'master_data.change_asset'


class DeleteAssetView(auth_mixins.PermissionRequiredMixin, views.DeleteView):
    model = Asset
    template_name = 'asset/asset_delete.html'
    success_url = reverse_lazy('assets_list')

    permission_required = 'master_data.change_asset'


class MaterialsListView(auth_mixins.PermissionRequiredMixin, views.ListView):
    model = Material
    template_name = 'material/materials.html'
    ordering = ('category', 'name')

    permission_required = 'master_data.view_material'


class CreateMaterialView(auth_mixins.PermissionRequiredMixin, views.CreateView):
    model = Material
    form_class = CreateMaterialForm
    template_name = 'material/material_create.html'
    success_url = reverse_lazy('materials_list')

    permission_required = 'master_data.add_material'


class EditMaterialView(auth_mixins.PermissionRequiredMixin, views.UpdateView):
    model = Material
    form_class = EditMaterialForm
    template_name = 'material/material_edit.html'
    success_url = reverse_lazy('materials_list')

    permission_required = 'master_data.change_material'


class DeleteMaterialView(auth_mixins.PermissionRequiredMixin, views.DeleteView):
    model = Material
    template_name = 'material/material_delete.html'
    success_url = reverse_lazy('materials_list')

    permission_required = 'master_data.change_material'


class MaterialCategoriesListView(auth_mixins.PermissionRequiredMixin, views.ListView):
    model = MaterialCategory
    template_name = 'material_category/material_categories.html'
    ordering = ('name',)

    permission_required = 'master_data.view_material_category'


class CreateMaterialCategoryView(auth_mixins.PermissionRequiredMixin, BootstrapFormViewMixin, views.CreateView):
    model = MaterialCategory
    fields = ('name', )
    template_name = 'material_category/material_category_create.html'
    success_url = reverse_lazy('material_categories_list')

    permission_required = 'master_data.add_material_category'


class EditMaterialCategoryView(auth_mixins.PermissionRequiredMixin, views.UpdateView):
    model = MaterialCategory
    form_class = EditMaterialCategoryForm
    template_name = 'material_category/material_category_edit.html'
    success_url = reverse_lazy('material_categories_list')

    permission_required = 'master_data.change_material_category'


class DeleteMaterialCategoryView(auth_mixins.PermissionRequiredMixin, views.DeleteView):
    model = MaterialCategory
    template_name = 'material_category/material_category_delete.html'
    success_url = reverse_lazy('material_categories_list')

    permission_required = 'master_data.change_material_category'


class BrandsListView(auth_mixins.PermissionRequiredMixin, views.ListView):
    model = Brand
    template_name = 'brands/brands.html'
    ordering = ('name',)

    permission_required = 'master_data.view_brand'


class CreateBrandView(auth_mixins.PermissionRequiredMixin, BootstrapFormViewMixin, views.CreateView):
    model = Brand
    fields = ('name', )
    template_name = 'brands/brand_create.html'
    success_url = reverse_lazy('brands_list')

    permission_required = 'master_data.add_brand'


class EditBrandView(auth_mixins.PermissionRequiredMixin, views.UpdateView):
    model = Brand
    form_class = EditBrandForm
    template_name = 'brands/brand_edit.html'
    success_url = reverse_lazy('brands_list')

    permission_required = 'master_data.change_brand'


class DeleteBrandView(auth_mixins.PermissionRequiredMixin, views.DeleteView):
    model = Brand
    template_name = 'brands/brand_delete.html'
    success_url = reverse_lazy('brands_list')

    permission_required = 'master_data.change_brand'


class AssetCategoriesListView(auth_mixins.PermissionRequiredMixin, views.ListView):
    model = AssetCategory
    template_name = 'asset_category/asset_categories.html'
    ordering = ('name',)

    permission_required = 'master_data.view_asset_category'


class CreateAssetCategoryView(auth_mixins.PermissionRequiredMixin, BootstrapFormViewMixin, views.CreateView):
    model = AssetCategory
    fields = ('name', )
    template_name = 'asset_category/asset_category_create.html'
    success_url = reverse_lazy('asset_categories_list')

    permission_required = 'master_data.add_asset_category'


class EditAssetCategoryView(auth_mixins.PermissionRequiredMixin, views.UpdateView):
    model = AssetCategory
    form_class = EditAssetCategoryForm
    template_name = 'asset_category/asset_category_edit.html'
    success_url = reverse_lazy('asset_categories_list')

    permission_required = 'master_data.change_asset_category'


class DeleteAssetCategoryView(auth_mixins.PermissionRequiredMixin, views.DeleteView):
    model = AssetCategory
    template_name = 'asset_category/asset_category_delete.html'
    success_url = reverse_lazy('asset_categories_list')

    permission_required = 'master_data.change_asset_category'
