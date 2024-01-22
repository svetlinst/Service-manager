import django.views.generic as views
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib.auth import mixins as auth_mixins
import re

from service_manager.core.views import BootstrapFormViewMixin
from service_manager.master_data.forms import CreateAssetForm, EditAssetForm, CreateMaterialForm, EditMaterialForm, \
    EditMaterialCategoryForm, EditBrandForm, EditAssetCategoryForm, EditSlaForm, CreateSlaForm, FilterAssetsForm, \
    FilterMaterialForm
from service_manager.master_data.models import Asset, Material, MaterialCategory, Brand, AssetCategory, SLA


class AssetsListView(auth_mixins.PermissionRequiredMixin, views.ListView):
    model = Asset
    template_name = 'asset/assets.html'
    ordering = ('category', 'brand', 'model_name', 'model_number')

    paginate_by = 10

    permission_required = 'master_data.view_asset'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        request = self.request.GET.copy()
        params = request.pop('page', True) and request.urlencode()
        context['params'] = params

        context['filter_form'] = FilterAssetsForm(self.request.GET or None)

        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        search_text = self.request.GET.get('search', None)
        if search_text:
            queryset = queryset.filter(
                Q(model_name__icontains=search_text) |
                Q(model_number__icontains=search_text) |
                Q(brand__name__icontains=search_text)
            )

        category = self.request.GET.get('category', None)
        if category:
            queryset = queryset.filter(category=category)

        return queryset


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
    ordering = ('category__name', 'name')

    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        request = self.request.GET.copy()
        params = request.pop('page', True) and request.urlencode()
        context['params'] = params

        context['filter_form'] = FilterMaterialForm(self.request.GET or None)

        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        search_text = self.request.GET.get('search', None)
        if search_text:
            queryset = queryset.filter(Q(name__icontains=search_text) | Q(category__name__icontains=search_text))

        category = self.request.GET.get('category', None)
        if category:
            queryset = queryset.filter(category=category)

        queryset = sorted(queryset, key=lambda x: (1 if re.match("^[А-ЯЁ]", x.category.name, re.IGNORECASE) else 2, x.category.name))

        return queryset

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
    # ordering = ('name',)

    paginate_by = 10

    permission_required = 'master_data.view_materialcategory'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        request = self.request.GET.copy()
        params = request.pop('page', True) and request.urlencode()
        context['params'] = params

        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        search_text = self.request.GET.get('search_value', None)
        if search_text:
            queryset = queryset.filter(name__icontains=search_text)
        return queryset


class CreateMaterialCategoryView(auth_mixins.PermissionRequiredMixin, BootstrapFormViewMixin, views.CreateView):
    model = MaterialCategory
    fields = ('name',)
    template_name = 'material_category/material_category_create.html'
    success_url = reverse_lazy('material_categories_list')

    permission_required = 'master_data.add_materialcategory'


class EditMaterialCategoryView(auth_mixins.PermissionRequiredMixin, views.UpdateView):
    model = MaterialCategory
    form_class = EditMaterialCategoryForm
    template_name = 'material_category/material_category_edit.html'
    success_url = reverse_lazy('material_categories_list')

    permission_required = 'master_data.change_materialcategory'


class DeleteMaterialCategoryView(auth_mixins.PermissionRequiredMixin, views.DeleteView):
    model = MaterialCategory
    template_name = 'material_category/material_category_delete.html'
    success_url = reverse_lazy('material_categories_list')

    permission_required = 'master_data.change_materialcategory'


class BrandsListView(auth_mixins.PermissionRequiredMixin, views.ListView):
    model = Brand
    template_name = 'brands/brands.html'
    ordering = ('name',)

    paginate_by = 10

    permission_required = 'master_data.view_brand'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        request = self.request.GET.copy()
        params = request.pop('page', True) and request.urlencode()
        context['params'] = params

        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        search_text = self.request.GET.get('search_value', None)
        if search_text:
            queryset = queryset.filter(name__icontains=search_text)
        return queryset


class CreateBrandView(auth_mixins.PermissionRequiredMixin, BootstrapFormViewMixin, views.CreateView):
    model = Brand
    fields = ('name',)
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

    paginate_by = 10

    permission_required = 'master_data.view_assetcategory'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        request = self.request.GET.copy()
        params = request.pop('page', True) and request.urlencode()
        context['params'] = params

        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        search_text = self.request.GET.get('search_value', None)
        if search_text:
            queryset = queryset.filter(name__icontains=search_text)
        return queryset


class CreateAssetCategoryView(auth_mixins.PermissionRequiredMixin, BootstrapFormViewMixin, views.CreateView):
    model = AssetCategory
    fields = ('name',)
    template_name = 'asset_category/asset_category_create.html'
    success_url = reverse_lazy('asset_categories_list')

    permission_required = 'master_data.add_assetcategory'


class EditAssetCategoryView(auth_mixins.PermissionRequiredMixin, views.UpdateView):
    model = AssetCategory
    form_class = EditAssetCategoryForm
    template_name = 'asset_category/asset_category_edit.html'
    success_url = reverse_lazy('asset_categories_list')

    permission_required = 'master_data.change_assetcategory'


class DeleteAssetCategoryView(auth_mixins.PermissionRequiredMixin, views.DeleteView):
    model = AssetCategory
    template_name = 'asset_category/asset_category_delete.html'
    success_url = reverse_lazy('asset_categories_list')

    permission_required = 'master_data.change_assetcategory'


class SlaListView(auth_mixins.PermissionRequiredMixin, views.ListView):
    model = SLA
    template_name = 'sla/service_level_agreements.html'
    ordering = ('name',)

    paginate_by = 10

    permission_required = 'master_data.view_sla'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        request = self.request.GET.copy()
        params = request.pop('page', True) and request.urlencode()
        context['params'] = params

        return context

    def get_queryset(self):
        queryset = super().get_queryset()

        search_text = self.request.GET.get('search_value', None)
        if search_text:
            queryset = queryset.filter(name__icontains=search_text)
        return queryset


class CreateSlaView(auth_mixins.PermissionRequiredMixin, views.CreateView):
    model = SLA
    form_class = CreateSlaForm
    template_name = 'sla/service_level_agreement_create.html'
    success_url = reverse_lazy('slas_list')

    permission_required = 'master_data.add_sla'


class EditSlaView(auth_mixins.PermissionRequiredMixin, views.UpdateView):
    model = SLA
    form_class = EditSlaForm
    template_name = 'sla/service_level_agreement_edit.html'
    success_url = reverse_lazy('slas_list')

    permission_required = 'master_data.change_sla'


class DeleteSlaView(auth_mixins.PermissionRequiredMixin, views.DeleteView):
    model = SLA
    template_name = 'sla/service_level_agreement_delete.html'
    success_url = reverse_lazy('slas_list')

    permission_required = 'master_data.change_sla'
