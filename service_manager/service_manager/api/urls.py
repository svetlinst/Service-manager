from django.urls import path
from service_manager.api.views import CustomerViewSet, ServiceRequestViewSet, CustomerNamesViewSet
from rest_framework import routers
from django.urls import path, include, re_path

router = routers.DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'service_requests', ServiceRequestViewSet)

urlpatterns = (
    path('', include(router.urls)),
    path('customers/names', CustomerNamesViewSet.as_view({'get': 'list'})),
)
