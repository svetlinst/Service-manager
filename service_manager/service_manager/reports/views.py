import datetime as dt
from django.db.models import Q
from django.shortcuts import render
import django.views.generic as views
from service_manager.main.models import ServiceOrderHeader


class FinishedOrdersListView(views.ListView):
    model = ServiceOrderHeader
    template_name = 'finished_orders.html'
    RELATED_ENTITIES = ['serviceordernote_set', 'serviceorderdetail_set', 'customer__customerasset_set', ]
    context_object_name = 'service_orders'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        request = self.request.GET.copy()
        params = request.pop('page', True) and request.urlencode()
        context['params'] = params
        context['orders_count'] = self.get_queryset().count()
        context['from_date'] = self.request.GET.get('from', '')
        context['to_date'] = self.request.GET.get('to', '')

        return context

    def get_queryset(self):
        date_from = self.request.GET.get('from', None)
        date_to = self.request.GET.get('to', None)

        query_set = ServiceOrderHeader.objects.filter(is_completed=True).prefetch_related(*self.RELATED_ENTITIES)
        if date_from and date_to:
            date_from = dt.datetime.strptime(date_from, '%Y-%m-%d')
            date_to = dt.datetime.strptime(date_to, '%Y-%m-%d')
            date_to += dt.timedelta(days=1)
            return query_set.filter(Q(completed_on__gte=date_from), Q(completed_on__lte=date_to))
        return query_set
