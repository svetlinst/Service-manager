from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
import service_manager.main.signals
from service_manager.main.views import ServiceOrderHeaderPendingServiceListView, \
    ServiceOrderHeaderDetailView, \
    CreateServiceOrderHeader, CreateServiceOrderDetailView, ServiceOrderDetailsListView, \
    EditServiceOrderDetailView, DeleteServiceOrderDetailView, complete_service_order, CreateServiceOrderNoteView, \
    ServiceOrderNotesListView, EditServiceOrderNoteView, DeleteServiceOrderNoteView, DeleteServiceOrderHeaderView, \
    ServiceOrderHeaderServicedListView, rollback_service_order, HandoverServiceOrderView, ServiceOrderNoteDetailView, \
    contact_us, TrackOrderDetailView, ServiceOrderPrintoutView, TrackOrderSearchFormView, CreateServiceOrderSuccess, \
    CustomerNotificationsListView, CreateCustomerNotificationView, EditCustomerNotificationView, \
    DeleteCustomerNotificationView, CustomerNotificationDetailView, HomeTemplateView

urlpatterns = [
                  path('', HomeTemplateView.as_view(), name='index'),
                  path('contact_us/', contact_us, name='contact_us'),
                  path('service_orders/pending/', ServiceOrderHeaderPendingServiceListView.as_view(),
                       name='service_orders_list_pending_service'),
                  path('service_orders/serviced/', ServiceOrderHeaderServicedListView.as_view(),
                       name='service_orders_list_serviced'),
                  path('service_order/<int:pk>/', ServiceOrderHeaderDetailView.as_view(), name='detail_service_order'),
                  path('service_order/customer/<int:customer_id>/asset/<int:asset_id>/create/',
                       CreateServiceOrderHeader.as_view(),
                       name='create_service_order'),
                  path('service_order/<int:pk>/success/', CreateServiceOrderSuccess.as_view(),
                       name='create_service_order_success'),
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
                  path('service_order/<int:order_id>/detail/<int:pk>/', ServiceOrderNoteDetailView.as_view(),
                       name='service_order_note_detail'),
                  path('service_order/<int:order_id>/service_note/edit/<int:pk>/', EditServiceOrderNoteView.as_view(),
                       name='edit_service_order_note'),
                  path('service_order/<int:order_id>/service_note/delete/<int:pk>/',
                       DeleteServiceOrderNoteView.as_view(), name='delete_service_order_note'),
                  path('service_order/<int:pk>/handover/', HandoverServiceOrderView.as_view(),
                       name='handover_service_order'),
                  path('service_order/<int:pk>/rollback/', rollback_service_order, name='rollback_service_order'),
                  path('service_order/track_order/<slug:slug>/', TrackOrderDetailView.as_view(), name='track_order'),
                  path('service_order/<int:pk>/customer_printout/', ServiceOrderPrintoutView.as_view(),
                       name='customer_printout'),
                  path('service_order/track_order_search/', TrackOrderSearchFormView.as_view(),
                       name='track_order_search'),
                  path('service_order/<int:order_id>/customer_notifications/', CustomerNotificationsListView.as_view(),
                       name='customer_notifications'),
                  path('service_order/<int:order_id>/customer_notifications/create/',
                       CreateCustomerNotificationView.as_view(), name='create_customer_notification'),
                  path('service_order/<int:order_id>/customer_notifications/<int:pk>/',
                       EditCustomerNotificationView.as_view(), name='edit_customer_notification'),
                  path('service_order/<int:order_id>/customer_notifications/delete/<int:pk>/',
                       DeleteCustomerNotificationView.as_view(), name='delete_customer_notification'),
                  path('service_order/<int:order_id>/customer_notifications/detail/<int:pk>/',
                       CustomerNotificationDetailView.as_view(), name='customer_notification_detail'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
