from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from service_manager.main.views import get_index, CustomersListView, EditCustomerView, CreateCustomerView

urlpatterns = [
                  path('', get_index, name='index'),
                  path('customers/', CustomersListView.as_view(), name='customers_list'),
                  path('customers/<int:pk>/', EditCustomerView.as_view(), name='edit_customer'),
                  path('customers/create/', CreateCustomerView.as_view(), name='create_customer'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
