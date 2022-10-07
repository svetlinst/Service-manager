from django.urls import path

from service_manager.customers.views import CustomersListView, EditCustomerView, CreateCustomerView, DeleteCustomerView, \
    CreateCustomerAssetView, EditCustomerAssetView, DeleteCustomerAssetView, \
    CreateCustomerRepresentativeView, EditCustomerRepresentativeView, DeleteCustomerRepresentativeView, \
    CreateCustomerDepartmentView, EditCustomerDepartmentView, DeleteCustomerDepartmentView, \
    CustomerDetailView

urlpatterns = [
    path('', CustomersListView.as_view(), name='customers_list'),
    path('detail/<int:pk>/', CustomerDetailView.as_view(), name='customer_detail'),
    path('<int:pk>/', EditCustomerView.as_view(), name='edit_customer'),
    path('create/', CreateCustomerView.as_view(), name='create_customer'),
    path('delete/<int:pk>', DeleteCustomerView.as_view(), name='delete_customer'),
    path('<int:customer_id>/customer_asset/create/', CreateCustomerAssetView.as_view(), name='create_customer_asset'),
    path('<int:customer_id>/customer_asset/<int:pk>/', EditCustomerAssetView.as_view(), name='edit_customer_asset'),
    path('<int:customer_id>/customer_asset/delete/<int:pk>/', DeleteCustomerAssetView.as_view(),
         name='delete_customer_asset'),
    path('<int:customer_id>/customer_representative/create/', CreateCustomerRepresentativeView.as_view(),
         name='create_customer_representative'),
    path('<int:customer_id>/customer_representative/<int:pk>/', EditCustomerRepresentativeView.as_view(),
         name='edit_customer_representative'),
    path('<int:customer_id>/customer_representative/delete/<int:pk>/', DeleteCustomerRepresentativeView.as_view(),
         name='delete_customer_representative'),
    path('<int:customer_id>/customer_department/create/', CreateCustomerDepartmentView.as_view(),
         name='create_customer_department'),
    path('<int:customer_id>/customer_department/edit/<int:pk>/', EditCustomerDepartmentView.as_view(),
         name='edit_customer_department'),
    path('<int:customer_id>/customer_department/delete/<int:pk>/', DeleteCustomerDepartmentView.as_view(),
         name='delete_customer_department'),
]
