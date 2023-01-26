from django.conf import settings


def get_protocol_and_domain_as_string():
    if len(settings.ALLOWED_HOSTS) == 2:
        # Local
        result = f'http://{settings.ALLOWED_HOSTS[1]}:8000'
    else:
        # Production
        result = f'https://{settings.ALLOWED_HOSTS[0]}'

    return result
