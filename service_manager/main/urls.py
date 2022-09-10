from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from service_manager.main.views import get_index, CustomersListView, CustomerUpdateView

urlpatterns = [
                  path('', get_index, name='index'),
                  path('customers/', CustomersListView.as_view(), name='customers_list'),
    path('customers/<int:pk>/', CustomerUpdateView.as_view(), name='customer_details'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
