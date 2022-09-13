from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from service_manager.main.views import get_index, CustomersListView, EditCustomerView, CreateCustomerView, \
    AssetsListView, CreateAssetView, EditAssetView, DeleteAssetView, DeleteCustomerView, MaterialsListView, \
    CreateMaterialView, EditMaterialView, DeleteMaterialView

urlpatterns = [
                  path('', get_index, name='index'),
                  path('customers/', CustomersListView.as_view(), name='customers_list'),
                  path('customers/<int:pk>/', EditCustomerView.as_view(), name='edit_customer'),
                  path('customers/create/', CreateCustomerView.as_view(), name='create_customer'),
                  path('assets/', AssetsListView.as_view(), name='assets_list'),
                  path('assets/create/', CreateAssetView.as_view(), name='create_asset'),
                  path('asset/<int:pk>/', EditAssetView.as_view(), name='edit_asset'),
                  path('asset/delete/<int:pk>/', DeleteAssetView.as_view(), name='delete_asset'),
                  path('customer/delete/<int:pk>', DeleteCustomerView.as_view(), name='delete_customer'),
                  path('materials/', MaterialsListView.as_view(), name='materials_list'),
                  path('materials/create/', CreateMaterialView.as_view(), name='create_material'),
                  path('material/<int:pk>/', EditMaterialView.as_view(), name='edit_material'),
                  path('material/delete/<int:pk>/', DeleteMaterialView.as_view(), name='delete_material'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
