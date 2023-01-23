from django.urls import path

from service_manager.master_data.views import AssetsListView, CreateAssetView, EditAssetView, DeleteAssetView, \
    MaterialsListView, CreateMaterialView, EditMaterialView, DeleteMaterialView, MaterialCategoriesListView, \
    EditMaterialCategoryView, DeleteMaterialCategoryView, CreateMaterialCategoryView, BrandsListView, CreateBrandView, \
    EditBrandView, DeleteBrandView, AssetCategoriesListView, CreateAssetCategoryView, EditAssetCategoryView, \
    DeleteAssetCategoryView, SlaListView, CreateSlaView, EditSlaView, DeleteSlaView

urlpatterns = [
    path('assets/', AssetsListView.as_view(), name='assets_list'),
    path('assets/create/', CreateAssetView.as_view(), name='create_asset'),
    path('assets/<int:pk>/', EditAssetView.as_view(), name='edit_asset'),
    path('assets/delete/<int:pk>/', DeleteAssetView.as_view(), name='delete_asset'),
    path('materials/', MaterialsListView.as_view(), name='materials_list'),
    path('materials/create/', CreateMaterialView.as_view(), name='create_material'),
    path('materials/<int:pk>/', EditMaterialView.as_view(), name='edit_material'),
    path('materials/delete/<int:pk>/', DeleteMaterialView.as_view(), name='delete_material'),
    path('material_categories/', MaterialCategoriesListView.as_view(), name='material_categories_list'),
    path('material_categories/create/', CreateMaterialCategoryView.as_view(), name='create_material_category'),
    path('material_categories/<int:pk>/', EditMaterialCategoryView.as_view(), name='edit_material_category'),
    path('material_categories/delete/<int:pk>/', DeleteMaterialCategoryView.as_view(), name='delete_material_category'),
    path('brands/', BrandsListView.as_view(), name='brands_list'),
    path('brands/create/', CreateBrandView.as_view(), name='create_brand'),
    path('brands/<int:pk>/', EditBrandView.as_view(), name='edit_brand'),
    path('brands/delete/<int:pk>/', DeleteBrandView.as_view(), name='delete_brand'),
    path('asset_cateogries/', AssetCategoriesListView.as_view(), name='asset_categories_list'),
    path('asset_categories/create/', CreateAssetCategoryView.as_view(), name='create_asset_category'),
    path('asset_categories/<int:pk>/', EditAssetCategoryView.as_view(), name='edit_asset_category'),
    path('asset_categories/delete/<int:pk>/', DeleteAssetCategoryView.as_view(), name='delete_asset_category'),
    path('sla/', SlaListView.as_view(), name='slas_list'),
    path('sla/create/', CreateSlaView.as_view(), name='create_sla'),
    path('sla/<int:pk>/', EditSlaView.as_view(), name='edit_sla'),
    path('sla/delete/<int:pk>/', DeleteSlaView.as_view(), name='delete_sla'),
]
