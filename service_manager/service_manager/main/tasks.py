from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string

from service_manager import settings
from service_manager.main.models import ServiceOrderHeader


@shared_task
def send_successful_service_order_creation_email(service_order_id):
    service_order_header = ServiceOrderHeader.objects.get(pk=service_order_id)
    user_mail = service_order_header.customer.email_address
    context = {
        'service_order': service_order_header,
    }

    message = render_to_string('email_templates/service_order_created.html', context)
    send_mail(
        subject='New Service order @ ServiceManager',
        message=None,
        html_message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user_mail],
    )
