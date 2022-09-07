from django.urls import path

from service_manager.main.views import get_index

urlpatterns = [
    path('', get_index, name='index')
]