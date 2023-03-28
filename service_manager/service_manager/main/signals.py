import datetime

from django.db.models.signals import post_save
from django.dispatch import receiver

from service_manager.main.models import ServiceOrderHeader, CustomerNotification
from service_manager.main.tasks import send_successful_service_order_creation_email


@receiver(post_save, sender=ServiceOrderHeader)
def service_order_header_created(sender, instance, created, **kwargs):
    if not created:
        return
    if instance.send_emails:
        # log information of the message sent in CustomerNotification table
        CustomerNotification.objects.create(
            notification_method=2,
            notified_on=datetime.datetime.now(),
            service_order=instance,
            notified_by=instance.accepted_by,
            service_order_current_status=instance.status,
        )

        send_successful_service_order_creation_email.delay(instance.pk)
