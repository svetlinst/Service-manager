from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from service_manager.main.views import get_index

urlpatterns = [
                  path('', get_index, name='index')
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
