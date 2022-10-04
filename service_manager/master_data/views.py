import django.views.generic as views
from django.urls import reverse_lazy
from django.contrib.auth import mixins as auth_mixins

from service_manager.core.views import BootstrapFormViewMixin
from service_manager.master_data.forms import CreateAssetForm, EditAssetForm, CreateMaterialForm, EditMaterialForm, \
    EditMaterialCategoryForm
from service_manager.master_data.models import Asset, Material, MaterialCategory


class AssetsListView(auth_mixins.LoginRequiredMixin, views.ListView):
    model = Asset
    template_name = 'asset/assets.html'
    ordering = ('category', 'brand', 'model_name', 'model_number')


class CreateAssetView(auth_mixins.LoginRequiredMixin, views.CreateView):
    model = Asset
    form_class = CreateAssetForm
    template_name = 'asset/asset_create.html'
    success_url = reverse_lazy('assets_list')


class EditAssetView(auth_mixins.LoginRequiredMixin, views.UpdateView):
    model = Asset
    form_class = EditAssetForm
    template_name = 'asset/asset_edit.html'
    success_url = reverse_lazy('assets_list')


class DeleteAssetView(auth_mixins.LoginRequiredMixin, views.DeleteView):
    model = Asset
    template_name = 'asset/asset_delete.html'
    success_url = reverse_lazy('assets_list')


class MaterialsListView(auth_mixins.LoginRequiredMixin, views.ListView):
    model = Material
    template_name = 'material/materials.html'
    ordering = ('category', 'name')


class CreateMaterialView(auth_mixins.LoginRequiredMixin, views.CreateView):
    model = Material
    form_class = CreateMaterialForm
    template_name = 'material/material_create.html'
    success_url = reverse_lazy('materials_list')


class EditMaterialView(auth_mixins.LoginRequiredMixin, views.UpdateView):
    model = Material
    form_class = EditMaterialForm
    template_name = 'material/material_edit.html'
    success_url = reverse_lazy('materials_list')


class DeleteMaterialView(auth_mixins.LoginRequiredMixin, views.DeleteView):
    model = Material
    template_name = 'material/material_delete.html'
    success_url = reverse_lazy('materials_list')


class MaterialCategoriesListView(auth_mixins.LoginRequiredMixin, views.ListView):
    model = MaterialCategory
    template_name = 'material_category/material_categories.html'
    ordering = ('-name',)


class CreateMaterialCategoryView(auth_mixins.LoginRequiredMixin, BootstrapFormViewMixin, views.CreateView):
    model = MaterialCategory
    fields = '__all__'
    template_name = 'material_category/material_category_create.html'
    success_url = reverse_lazy('material_categories_list')


class EditMaterialCategoryView(auth_mixins.LoginRequiredMixin, views.UpdateView):
    model = MaterialCategory
    form_class = EditMaterialCategoryForm
    template_name = 'material_category/material_category_edit.html'
    success_url = reverse_lazy('material_categories_list')


class DeleteMaterialCategoryView(auth_mixins.LoginRequiredMixin, views.DeleteView):
    model = MaterialCategory
    template_name = 'material_category/material_category_delete.html'
    success_url = reverse_lazy('material_categories_list')
