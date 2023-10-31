from django.urls import path

from service_manager.service_requests.views import ServiceRequestsListView, ServiceRequestDetailView, CreateServiceRequestView, \
    EditServiceRequestView, ServiceRequestAssignHandlerView, ServiceRequestUpdateResolutionView, \
    DeleteServiceRequestView, finalize_service_request, reject_service_request, ServiceRequestCreateServiceOrder

urlpatterns = [
    path('/', ServiceRequestsListView.as_view(), name='service_requests'),
    path('/detail/<int:pk>/', ServiceRequestDetailView.as_view(),
         name='service_request_detail'),
    path('/create/', CreateServiceRequestView.as_view(), name='create_service_request'),
    path('/<int:pk>/', EditServiceRequestView.as_view(), name='edit_service_request'),
    path('/<int:pk>/assign_handler/', ServiceRequestAssignHandlerView.as_view(),
         name='service_request_assign_handler'),
    path('/<int:pk>/update_resolution/', ServiceRequestUpdateResolutionView.as_view(),
         name='service_request_update_resolution'),
    path('/delete/<int:pk>/', DeleteServiceRequestView.as_view(),
         name='delete_service_request'),
    path('/<int:pk>/finalize/', finalize_service_request,
         name='finalize_service_request'),
    path('/<int:pk>/reject/', reject_service_request, name='reject_service_request'),
    path('/<int:pk>/create_service_order/<int:customer_id>/',
         ServiceRequestCreateServiceOrder.as_view(),
         name='service_request_create_order')
]