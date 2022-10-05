from django.shortcuts import render
import django.views.generic as views

from service_manager.main.models import ServiceOrderHeader


class FinishedOrdersListView(views.ListView):
    model = ServiceOrderHeader
    template_name = 'finished_orders.html'
    RELATED_ENTITIES = ['serviceordernote_set', 'serviceorderdetail_set', 'customer__customerasset_set', ]

    def get_queryset(self):
        return ServiceOrderHeader.objects.filter(is_completed=True).prefetch_related(*self.RELATED_ENTITIES)
