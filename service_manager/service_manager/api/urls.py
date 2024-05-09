from django.urls import path
from service_manager.api.views import CustomerViewSet
from rest_framework import routers
from django.urls import path, include, re_path

router = routers.DefaultRouter()
router.register(r'customers', CustomerViewSet)

urlpatterns = (
    path('', include(router.urls)),
)
