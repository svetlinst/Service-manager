from django.urls import path

from service_manager.reports.views import FinishedOrdersListView

urlpatterns = [
    path('finished_orders/', FinishedOrdersListView.as_view(), name='finished_orders'),
]