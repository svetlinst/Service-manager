from django.contrib.auth import models as auth_models
from django.contrib.auth.models import PermissionsMixin
from django.db import models

from service_manager.accounts.managers import AppUserManager
from django.utils.translation import gettext_lazy as _


class AppUser(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    email = models.EmailField(
        unique=True,
        null=False,
        blank=False,
        verbose_name=_('email'),
    )

    is_staff = models.BooleanField(
        default=False,
    )

    date_joined = models.DateTimeField(
        auto_now_add=True,
    )

    is_active = models.BooleanField(
        default=True,
    )

    USERNAME_FIELD = 'email'

    @property
    def profile_full_name(self):
        profile = Profile.objects.filter(pk=self.pk)
        if profile:
            return profile[0].full_name
        return self.email

    objects = AppUserManager()

    def __str__(self):
        return self.profile_full_name


class Profile(models.Model):
    FIRST_NAME_MAX_LENGTH = 20
    LAST_NAME_MAX_LENGTH = 20
    PHONE_NUMBER_MAX_LENGTH = 20

    first_name = models.CharField(
        _('first_name'),
        max_length=FIRST_NAME_MAX_LENGTH,
        null=False,
        blank=False,
    )

    last_name = models.CharField(
        _('last_name'),
        max_length=LAST_NAME_MAX_LENGTH,
        null=False,
        blank=False,
    )

    phone_number = models.CharField(
        _('phone_number'),
        max_length=PHONE_NUMBER_MAX_LENGTH,
        null=True,
        blank=True,
    )

    app_user = models.OneToOneField(
        AppUser,
        on_delete=models.CASCADE,
        primary_key=True,
        verbose_name=_('app_user'),
    )

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.full_name
