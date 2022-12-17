from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from service_manager.accounts.models import AppUser, Profile

User = get_user_model()


@admin.register(User)
class AppUserAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        """
        Grant accesses to all users with is_staff permissions to the below groups.
        Don't allow them to change any other settings.
        """
        super().save_model(request, obj, form, change)

        groups = ['FrontOffice', 'BackOffice', 'MasterDataEditor', ]
        if obj.is_staff:
            form.cleaned_data['groups'] = Group.objects.filter(name__in=groups)


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['first_name']
