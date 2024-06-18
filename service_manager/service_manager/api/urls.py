from service_manager.api.views import CustomerViewSet, ServiceRequestViewSet, CustomerNamesViewSet, UserDetailApiView, \
    ProfileViewSet
from rest_framework import routers
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)


router = routers.DefaultRouter()
router.register(r'customers', CustomerViewSet)
router.register(r'service_requests', ServiceRequestViewSet)

urlpatterns = (
    path('', include(router.urls)),
    path('customers/names', CustomerNamesViewSet.as_view({'get': 'list'})),
    path('profiles/<int:id>/', ProfileViewSet.as_view({'get': 'retrieve', 'patch': 'partial_update'})),
    path('users/<str:email>/', UserDetailApiView.as_view()),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),
)
