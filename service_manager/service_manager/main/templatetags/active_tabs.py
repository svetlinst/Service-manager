from django import template
from service_manager.master_data.urls import urlpatterns as master_data_url_patterns
from service_manager.customers.urls import urlpatterns as customers_url_patterns
from service_manager.main.urls import urlpatterns as main_url_patterns
from service_manager.reports.urls import urlpatterns as reports_url_patterns

register = template.Library()

GROUP_NAMES = {
    'main': main_url_patterns,
    'reports': reports_url_patterns,
    'customers': customers_url_patterns,
    'master_data': master_data_url_patterns,
}

# todo: handle active tab selection with JS
COMMON_TABS = ['index', 'contact_us', 'service_requests', 'create_service_request']


@register.filter(name='is_active_nav_link')
def is_active_nav_link(url_path, tab_group_name):
    is_active = False

    url_patterns = GROUP_NAMES[tab_group_name]

    url_pattern_names = [x.name for x in url_patterns if x.name not in COMMON_TABS]

    if url_path in url_pattern_names:
        is_active = True

    return is_active
