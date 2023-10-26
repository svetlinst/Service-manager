from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework import routers

from . import views

urlpatterns = [
    path('', include('rest_framework.urls')),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    # path('service_orders/', ListServiceOrderHeadersViewSet.as_view(), name='service_orders_all'),

]

router = routers.DefaultRouter()
router.register('service_orders', views.ListServiceOrderHeadersViewSet)

urlpatterns += router.urls
