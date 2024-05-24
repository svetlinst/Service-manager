from django import template
from service_manager.main.models import ServiceRequest

register = template.Library()


@register.simple_tag()
def get_status_value(key):
    choices = ServiceRequest.TYPE_CHOICES
    choice = [x for x in choices if x[0] == key][0]
    return choice[1]
