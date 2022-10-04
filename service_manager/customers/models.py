from django.core.validators import EmailValidator
from django.db import models

from service_manager.core.models import BaseAuditEntity
from service_manager.master_data.models import Asset, CustomerType


class Customer(BaseAuditEntity):
    NAME_MAX_LENGTH = 100
    VAT_MAX_LENGTH = 20
    EMAIL_MAX_LENGTH = 254
    PHONE_NUMBER_MAX_LENGTH = 20

    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
    )

    vat = models.CharField(
        max_length=VAT_MAX_LENGTH,
        null=True,
        blank=True,
    )

    email_address = models.EmailField(
        max_length=EMAIL_MAX_LENGTH,
        validators=(
            EmailValidator,
        )
    )

    phone_number = models.CharField(
        max_length=PHONE_NUMBER_MAX_LENGTH,
    )

    type = models.ForeignKey(
        CustomerType,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return self.name


class CustomerRepresentative(BaseAuditEntity):
    FIRST_NAME_MAX_LENGTH = 20
    LAST_NAME_MAX_LENGTH = 20
    EMAIL_ADDRESS_MAX_LENGTH = 254
    PHONE_NUMBER_MAX_LENGTH = 20

    first_name = models.CharField(
        max_length=FIRST_NAME_MAX_LENGTH,
    )

    last_name = models.CharField(
        max_length=LAST_NAME_MAX_LENGTH,
    )

    email_address = models.CharField(
        max_length=EMAIL_ADDRESS_MAX_LENGTH,
        validators=(
            EmailValidator,
        ),
        null=True,
        blank=True,
    )

    phone_number = models.CharField(
        max_length=PHONE_NUMBER_MAX_LENGTH,
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        ordering = ('first_name', 'last_name',)


class CustomerDepartment(BaseAuditEntity):
    NAME_MAX_LENGTH = 100

    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{str(self.customer)} {self.name}'

    class Meta:
        ordering = ('name',)


class CustomerAsset(BaseAuditEntity):
    SERIAL_NUMBER_MAX_LENGTH = 20
    PRODUCT_NUMBER_MAX_LENGTH = 20

    serial_number = models.CharField(
        max_length=SERIAL_NUMBER_MAX_LENGTH,
        null=True,
        blank=True,
    )

    product_number = models.CharField(
        max_length=PRODUCT_NUMBER_MAX_LENGTH,
        null=True,
        blank=True,
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
    )

    asset = models.ForeignKey(
        Asset,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{str(self.customer)}---{str(self.asset)}--{self.serial_number}---{self.product_number}'

    class Meta:
        ordering = ('asset__category__name', 'asset__brand__name', 'asset__model_name', 'serial_number',)
