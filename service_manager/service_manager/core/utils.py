from django.conf import settings
from django.db.models import Q

from service_manager.master_data.models import Material


def get_protocol_and_domain_as_string():
    if len(settings.ALLOWED_HOSTS) == 2:
        # Local
        result = f'http://{settings.ALLOWED_HOSTS[1]}:8000'
    else:
        # Production
        result = f'https://{settings.ALLOWED_HOSTS[0]}'

    return result


def get_material_count_matching_conditions(category_request, search_request):
    materials = Material.objects.all()

    category = category_request
    if category:
        materials = materials.filter(category=category)

    search = search_request
    if search:
        materials = materials.filter(Q(name__icontains=search) | Q(category__name__icontains=search))

    return materials.count()
