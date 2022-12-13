from django import template

from service_manager.main.models import ServiceOrderHeader

register = template.Library()


@register.filter(name='soh_is_completed_without_notes')
def soh_is_completed_without_notes(service_order_id):
    service_order = ServiceOrderHeader.objects.get(pk=service_order_id)

    if service_order.is_completed and not service_order.serviceordernote_set.all():
        return True
    return False
