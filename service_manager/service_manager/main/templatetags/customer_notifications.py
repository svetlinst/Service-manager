from django import template
from service_manager.main.models import CustomerNotification

register = template.Library()


@register.simple_tag()
def get_notification_value(key):
    choices = CustomerNotification.TYPE_CHOICES
    choice = [x for x in choices if x[0] == int(key)][0]
    return choice[1]
