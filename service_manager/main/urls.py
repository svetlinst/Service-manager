from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from service_manager.main import views
from service_manager.main.views import get_index, CustomersListView, EditCustomerView, CreateCustomerView, \
    AssetsListView, CreateAssetView, EditAssetView, DeleteAssetView, DeleteCustomerView, MaterialsListView, \
    CreateMaterialView, EditMaterialView, DeleteMaterialView, CreateCustomerAssetView, EditCustomerAssetView, \
    DeleteCustomerAssetView, ServiceOrderHeaderPendingServiceListView, ServiceOrderHeaderDetailView, \
    CreateServiceOrderHeader, \
    CustomerRepresentativesListView, CreateCustomerRepresentativeView, EditCustomerRepresentativeView, \
    DeleteCustomerRepresentativeView, CreateServiceOrderDetailView, ServiceOrderDetailsListView, \
    EditServiceOrderDetailView, DeleteServiceOrderDetailView, complete_service_order, CustomerDepartmentsListView, \
    CreateCustomerDepartmentView, EditCustomerDepartmentView, DeleteCustomerDepartmentView, CreateServiceOrderNoteView, \
    ServiceOrderNotesListView, EditServiceOrderNoteView, DeleteServiceOrderNoteView, DeleteServiceOrderHeaderView, \
    ServiceOrderHeaderServicedListView

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
                  path('customer/<int:customer_id>/customer_asset/create/', CreateCustomerAssetView.as_view(),
                       name='create_customer_asset'),
                  path('customer/<int:customer_id>/customer_asset/<int:pk>/', EditCustomerAssetView.as_view(),
                       name='edit_customer_asset'),
                  path('customer/<int:customer_id>/customer_asset/delete/<int:pk>/', DeleteCustomerAssetView.as_view(),
                       name='delete_customer_asset'),
                  path('service_orders/pending/', ServiceOrderHeaderPendingServiceListView.as_view(),
                       name='service_orders_list_pending_service'),
                  path('service_orders/serviced/', ServiceOrderHeaderServicedListView.as_view(),
                       name='service_orders_list_serviced'),
                  path('service_order/<int:pk>/', ServiceOrderHeaderDetailView.as_view(), name='detail_service_order'),
                  path('service_order/customer/<int:customer_id>/asset/<int:asset_id>/create/',
                       CreateServiceOrderHeader.as_view(),
                       name='create_service_order'),
                  path('service_order/delete/<int:pk>/', DeleteServiceOrderHeaderView.as_view(),
                       name='delete_service_order'),
                  path('ajax/load_customer_represenatives/', views.load_customer_representatives,
                       name='ajax_load_customer_representatives'),
                  path('customer/<int:customer_id>/customer_representatives/',
                       CustomerRepresentativesListView.as_view(),
                       name='customer_representatives_list'),
                  path('customer/<int:customer_id>/customer_representative/create/',
                       CreateCustomerRepresentativeView.as_view(),
                       name='create_customer_representative'),
                  path('customer/<int:customer_id>/customer_representative/<int:pk>/',
                       EditCustomerRepresentativeView.as_view(),
                       name='edit_customer_representative'),
                  path('customer/<int:customer_id>/customer_representative/delete/<int:pk>/',
                       DeleteCustomerRepresentativeView.as_view(),
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
                  path('customer/<int:customer_id>/customer_departments/', CustomerDepartmentsListView.as_view(),
                       name='customer_department'),
                  path('customer/<int:customer_id>/customer_department/create/', CreateCustomerDepartmentView.as_view(),
                       name='create_customer_department'),
                  path('customer/<int:customer_id>/customer_department/edit/<int:pk>/',
                       EditCustomerDepartmentView.as_view(), name='edit_customer_department'),
                  path('customer/<int:customer_id>/customer_department/delete/<int:pk>/',
                       DeleteCustomerDepartmentView.as_view(),
                       name='delete_customer_department'),
                  path('service_order/<int:order_id>/service_notes/create', CreateServiceOrderNoteView.as_view(),
                       name='create_service_order_note'),
                  path('service_order/<int:order_id>/service_notes/', ServiceOrderNotesListView.as_view(),
                       name='service_order_notes'),
                  path('service_order/<int:order_id>/service_note/edit/<int:pk>/', EditServiceOrderNoteView.as_view(),
                       name='edit_service_order_note'),
                  path('service_order/<int:order_id>/service_note/delete/<int:pk>/',
                       DeleteServiceOrderNoteView.as_view(), name='delete_service_order_note'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
