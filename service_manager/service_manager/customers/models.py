from django.core.validators import EmailValidator
from django.db import models

from service_manager.core.models import BaseAuditEntity, ActiveModel
from service_manager.customers.validators import numbers_only_validator, phone_number_validator
from service_manager.master_data.models import Asset, CustomerType
from django.utils.translation import gettext_lazy as _


class Customer(ActiveModel, BaseAuditEntity):
    NAME_MAX_LENGTH = 100
    VAT_MAX_LENGTH = 20
    EMAIL_MAX_LENGTH = 254
    PHONE_NUMBER_MAX_LENGTH = 20

    name = models.CharField(
        _('name'),
        max_length=NAME_MAX_LENGTH,
    )

    vat = models.CharField(
        _('vat'),
        max_length=VAT_MAX_LENGTH,
        null=True,
        blank=True,
        validators=[
            numbers_only_validator,
        ],
    )

    email_address = models.EmailField(
        _('email_address'),
        max_length=EMAIL_MAX_LENGTH,
        validators=(
            EmailValidator,
        )
    )

    phone_number = models.CharField(
        _('phone_number'),
        max_length=PHONE_NUMBER_MAX_LENGTH,
        validators=(
            phone_number_validator,
        )
    )

    type = models.ForeignKey(
        CustomerType,
        on_delete=models.CASCADE,
        verbose_name=_('type'),
    )

    has_subscription = models.BooleanField(
        _('has subscription'),
        default=0,
        null=False,
        blank=False,
    )

    is_regular_customer = models.BooleanField(
        _('is regular customer'),
        default=0,
        null=False,
        blank=False,
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('is_regular_customer', 'name',)


class CustomerRepresentative(ActiveModel, BaseAuditEntity):
    FIRST_NAME_MAX_LENGTH = 20
    LAST_NAME_MAX_LENGTH = 20
    EMAIL_ADDRESS_MAX_LENGTH = 254
    PHONE_NUMBER_MAX_LENGTH = 20

    first_name = models.CharField(
        _('first_name'),
        max_length=FIRST_NAME_MAX_LENGTH,
    )

    last_name = models.CharField(
        _('last_name'),
        max_length=LAST_NAME_MAX_LENGTH,
    )

    email_address = models.EmailField(
        _('email_address'),
        max_length=EMAIL_ADDRESS_MAX_LENGTH,
        validators=(
            EmailValidator,
        ),
        null=True,
        blank=True,
    )

    phone_number = models.CharField(
        _('phone_number'),
        max_length=PHONE_NUMBER_MAX_LENGTH,
        validators=[
            phone_number_validator,
        ]
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        verbose_name=_('customer'),
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        ordering = ('first_name', 'last_name',)


class CustomerDepartment(ActiveModel, BaseAuditEntity):
    NAME_MAX_LENGTH = 100

    name = models.CharField(
        _('name'),
        max_length=NAME_MAX_LENGTH,
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        verbose_name=_('customer'),
    )

    def __str__(self):
        return f'{self.name}'

    class Meta:
        ordering = ('name',)


class CustomerAsset(ActiveModel, BaseAuditEntity):
    SERIAL_NUMBER_MAX_LENGTH = 20
    PRODUCT_NUMBER_MAX_LENGTH = 20
    INVENTORY_NUMBER_MAX_LENGTH = 20
    LOCATION_MAX_LENGTH = 256

    serial_number = models.CharField(
        _('serial_number'),
        max_length=SERIAL_NUMBER_MAX_LENGTH,
        null=True,
        blank=True,
    )

    product_number = models.CharField(
        _('product_number'),
        max_length=PRODUCT_NUMBER_MAX_LENGTH,
        null=True,
        blank=True,
    )

    inventory_number = models.CharField(
        _('inventory_number'),
        max_length=INVENTORY_NUMBER_MAX_LENGTH,
        null=True,
        blank=True,
    )

    location = models.CharField(
        _('location'),
        max_length=LOCATION_MAX_LENGTH,
        null=True,
        blank=True,
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        verbose_name=_('customer'),
    )

    asset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
        verbose_name=_('asset'),
    )

    def __str__(self):
        return f'{str(self.customer)}---{str(self.asset)}--{self.serial_number}---{self.product_number}'

    class Meta:
        ordering = ('asset__category__name', 'asset__brand__name', 'asset__model_name', 'serial_number',)
