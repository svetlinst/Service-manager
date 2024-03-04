from celery import shared_task
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils import translation

from service_manager import settings
from service_manager.core.utils import get_protocol_and_domain_as_string
from service_manager.main.models import ServiceOrderHeader, ServiceRequest
from django.utils.translation import gettext_lazy as _


@shared_task
def send_successful_service_order_creation_email(service_order_id):
    service_order_header = ServiceOrderHeader.objects.get(pk=service_order_id)
    user_mail = service_order_header.customer.email_address

    protocol_domain = get_protocol_and_domain_as_string()

    context = {
        'service_order': service_order_header,
        'protocol_domain': protocol_domain,
    }

    cur_language = translation.get_language()

    try:
        translation.activate('bg')
        message = render_to_string('email_templates/service_order_created.html', context)
        send_mail(
            subject='New Service order @ ServiceManager',
            message=None,
            html_message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[user_mail],
        )
    finally:
        translation.activate(cur_language)

@shared_task()
def send_internal_service_order_creation_email(service_order_id, service_type:str):
    if service_type == 'order':
        service = ServiceOrderHeader.objects.get(pk=service_order_id)
        template_name = 'email_templates/internal_soh_created.html'
        subject = _('New Service Order in ServiceManager')
    else:
        service = ServiceRequest.objects.get(pk=service_order_id)
        template_name = 'email_templates/internal_service_request_created.html'
        subject = _('New Service Request in ServiceManager')

    protocol_domain = get_protocol_and_domain_as_string()

    context = {
        'service': service,
        'protocol_domain': protocol_domain,
    }

    cur_language = translation.get_language()

    try:
        translation.activate('bg')
        message = render_to_string(template_name=template_name, context=context)
        send_mail(
            subject=subject,
            message=None,
            html_message=message,
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[settings.INTERNAL_NOTIFICATION_EMAIL],
        )
    finally:
        translation.activate(cur_language)


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
