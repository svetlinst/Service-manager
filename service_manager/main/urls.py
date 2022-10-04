from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from service_manager.main.views import get_index, ServiceOrderHeaderPendingServiceListView, \
    ServiceOrderHeaderDetailView, \
    CreateServiceOrderHeader, CreateServiceOrderDetailView, ServiceOrderDetailsListView, \
    EditServiceOrderDetailView, DeleteServiceOrderDetailView, complete_service_order, CreateServiceOrderNoteView, \
    ServiceOrderNotesListView, EditServiceOrderNoteView, DeleteServiceOrderNoteView, DeleteServiceOrderHeaderView, \
    ServiceOrderHeaderServicedListView, handover_service_order, rollback_service_order

urlpatterns = [
                  path('', get_index, name='index'),
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
                  path('service_order/<int:order_id>/service_notes/create', CreateServiceOrderNoteView.as_view(),
                       name='create_service_order_note'),
                  path('service_order/<int:order_id>/service_notes/', ServiceOrderNotesListView.as_view(),
                       name='service_order_notes'),
                  path('service_order/<int:order_id>/service_note/edit/<int:pk>/', EditServiceOrderNoteView.as_view(),
                       name='edit_service_order_note'),
                  path('service_order/<int:order_id>/service_note/delete/<int:pk>/',
                       DeleteServiceOrderNoteView.as_view(), name='delete_service_order_note'),
                  path('service_order/<int:order_id>/handover/', handover_service_order, name='handover_service_order'),
                  path('service_order/<int:pk>/rollback/', rollback_service_order, name='rollback_service_order'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
