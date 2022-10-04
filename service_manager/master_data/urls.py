from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from service_manager.master_data.views import AssetsListView, CreateAssetView, EditAssetView, DeleteAssetView, \
    MaterialsListView, CreateMaterialView, EditMaterialView, DeleteMaterialView

urlpatterns = [
    path('assets/', AssetsListView.as_view(), name='assets_list'),
    path('assets/create/', CreateAssetView.as_view(), name='create_asset'),
    path('asset/<int:pk>/', EditAssetView.as_view(), name='edit_asset'),
    path('asset/delete/<int:pk>/', DeleteAssetView.as_view(), name='delete_asset'),
    path('materials/', MaterialsListView.as_view(), name='materials_list'),
    path('materials/create/', CreateMaterialView.as_view(), name='create_material'),
    path('material/<int:pk>/', EditMaterialView.as_view(), name='edit_material'),
    path('material/delete/<int:pk>/', DeleteMaterialView.as_view(), name='delete_material'),
]
