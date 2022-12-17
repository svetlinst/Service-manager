from celery import shared_task
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User


@shared_task
def send_password_reset_email_async(subject_template_name, email_template_name, context,
                                    from_email, to_email, html_email_template_name):
    user_model = get_user_model()
    context['user'] = user_model.objects.get(pk=context['user'])

    PasswordResetForm.send_mail(
        None,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name
    )
