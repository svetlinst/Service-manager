from django.urls import path

from service_manager.master_data.views import AssetsListView, CreateAssetView, EditAssetView, DeleteAssetView, \
    MaterialsListView, CreateMaterialView, EditMaterialView, DeleteMaterialView, MaterialCategoriesListView, \
    EditMaterialCategoryView, DeleteMaterialCategoryView, CreateMaterialCategoryView

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
]
