from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Service Manager API",
        default_version='v.0.0.0',
        description="API used for accessing Service Manager's information via API",
        contact=openapi.Contact(email="svetlinst@gmail.com"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)