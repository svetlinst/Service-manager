from django.conf import settings


def get_protocol_and_domain_as_string():
    if isinstance(settings.ALLOWED_HOSTS, list):
        # Local
        result = f'http://{settings.ALLOWED_HOSTS[1]}:8000'
    else:
        # Production
        result = f'https://{settings.ALLOWED_HOSTS}'

    return result
