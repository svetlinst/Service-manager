from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from service_manager.main import views
from service_manager.main.views import get_index, CustomersListView, EditCustomerView, CreateCustomerView, \
    AssetsListView, CreateAssetView, EditAssetView, DeleteAssetView, DeleteCustomerView, MaterialsListView, \
    CreateMaterialView, EditMaterialView, DeleteMaterialView, CreateCustomerAssetView, EditCustomerAssetView, \
    DeleteCustomerAssetView, ServiceOrderHeaderListView, ServiceOrderHeaderDetailView, CreateServiceOrderHeader, \
    CustomerRepresentativesListView, CreateCustomerRepresentativeView, EditCustomerRepresentativeView, \
    DeleteCustomerRepresentativeView, CreateServiceOrderDetailView, ServiceOrderDetailsListView, \
    EditServiceOrderDetailView, DeleteServiceOrderDetailView, complete_service_order

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
                  path('customer_asset/create/', CreateCustomerAssetView.as_view(), name='create_customer_asset'),
                  path('customer_asset/<int:pk>/', EditCustomerAssetView.as_view(), name='edit_customer_asset'),
                  path('customer_asset/delete/<int:pk>/', DeleteCustomerAssetView.as_view(),
                       name='delete_customer_asset'),
                  path('service_orders/', ServiceOrderHeaderListView.as_view(), name='service_orders_list'),
                  path('service_order/<int:pk>/', ServiceOrderHeaderDetailView.as_view(), name='detail_service_order'),
                  path('service_order/create/', CreateServiceOrderHeader.as_view(), name='create_service_order'),
                  path('ajax/load_customer_represenatives/', views.load_customer_representatives,
                       name='ajax_load_customer_representatives'),
                  path('customer_representatives/', CustomerRepresentativesListView.as_view(),
                       name='customer_representatives_list'),
                  path('customer_representative/create/', CreateCustomerRepresentativeView.as_view(),
                       name='create_customer_representative'),
                  path('customer_representative/<int:pk>/', EditCustomerRepresentativeView.as_view(),
                       name='edit_customer_representative'),
                  path('customer_representative/delete/<int:pk>/', DeleteCustomerRepresentativeView.as_view(),
                       name='delete_customer_representative'),
                  path('service_order/<int:order_id>/service_order_detail/create/',
                       CreateServiceOrderDetailView.as_view(),
                       name='create_service_order_detail'),
                  path('service_order/<int:order_id>/service_order_details/', ServiceOrderDetailsListView.as_view(),
                       name='service_order_details'),
                  path('service_order/<int:order_id>/service_order_detail/edit/<int:pk>/',
                       EditServiceOrderDetailView.as_view(),
                       name='edit_service_order_detail'),
                  path('service_order/<int:order_id>/service_order_detail/delete/<int:pk>/',
                       DeleteServiceOrderDetailView.as_view(),
                       name='delete_service_order_detail'),
                  path('service_order/<int:pk>/complete/', complete_service_order, name='complete_service_order'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
