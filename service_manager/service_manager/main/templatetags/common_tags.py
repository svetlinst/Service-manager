from django import template

from service_manager.main.models import ServiceOrderHeader

register = template.Library()


@register.filter(name='soh_is_completed_or_deleted_without_notes')
def soh_is_completed_or_deleted_without_notes(service_order_id):
    service_order = ServiceOrderHeader.objects.get(pk=service_order_id)

    if service_order.is_completed and not service_order.serviceordernote_set.all():
        return True
    if not service_order.active and not service_order.serviceordernote_set.all():
        return True
    return False


@register.simple_tag(takes_context=True)
def get_query_string_params(context, **kwargs):
    query_params = context['request'].GET.copy()
    for k, v in kwargs.items():
        query_params[k] = v

    return query_params.urlencode()
