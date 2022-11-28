from django import template

register = template.Library()


@register.filter(name='user_has_master_data_permissions')
def user_has_master_data_permissions(user):
    master_data_permissions = (
        'master_data.view_asset',
        'master_data.view_assetcategory',
        'master_data.view_brand',
        'master_data.view_material',
        'master_data.view_materialcategory',
    )
    has_permission = False

    for p in master_data_permissions:
        if user.has_perm(p):
            has_permission = True
            break

    return has_permission
