from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string

from service_manager import settings
from service_manager.main.models import ServiceOrderHeader


@shared_task
def send_successful_service_order_creation_email(service_order_id):
    service_order_header = ServiceOrderHeader.objects.get(pk=service_order_id)
    user_mail = service_order_header.customer.email_address
    tracking_url = f'test'
    allowed_hosts = settings.ALLOWED_HOSTS

    if isinstance(allowed_hosts, list):
        domain = f'{allowed_hosts[1]}:8000'
        protocol = 'http'
    else:
        protocol = 'https'
        domain = allowed_hosts

    context = {
        'service_order': service_order_header,
        'tracking_url': tracking_url,
        'domain': domain,
        'protocol': protocol,
    }

    message = render_to_string('email_templates/service_order_created.html', context)
    send_mail(
        subject='New Service order @ ServiceManager',
        message=None,
        html_message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user_mail],
    )


@shared_task()
def send_contact_us_email(email_data):
    message = render_to_string('email_templates/contact_us_mail_template.html', email_data)
    send_mail(
        subject='Support request @ ServiceManager',
        message=None,
        html_message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[settings.SUPPORT_EMAIL],
    )
