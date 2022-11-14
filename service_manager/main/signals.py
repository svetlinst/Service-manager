from django.db.models.signals import post_save
from django.dispatch import receiver

from service_manager.main.models import ServiceOrderHeader
from service_manager.main.tasks import send_successful_service_order_creation_email


@receiver(post_save, sender=ServiceOrderHeader)
def service_order_header_created(sender, instance, created, **kwargs):
    if not created:
        return
    send_successful_service_order_creation_email.delay(instance.pk)
