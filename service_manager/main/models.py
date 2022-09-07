from django.core.validators import EmailValidator
from django.db import models


class AuditEntity(models.Model):
    created_on = models.DateTimeField(
        auto_now_add=True,
    )

    updated_on = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        abstract = True


class CustomerType(AuditEntity):
    NAME_MAX_LENGTH = 50

    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
    )

    class Meta:
        db_table = 'main_customer_type'


class Customer(AuditEntity):
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


class CustomerRepresentative(AuditEntity):
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
        )
    )

    phone_number = models.CharField(
        max_length=PHONE_NUMBER_MAX_LENGTH,
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = 'main_customer_representative'


class CustomerDepartment(AuditEntity):
    NAME_MAX_LENGTH = 100

    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
    )

    class Meta:
        db_table = 'main_customer_department'


class Brand(AuditEntity):
    NAME_MAX_LENGTH = 100

    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
    )


class AssetCategory(AuditEntity):
    NAME_MAX_LENGTH = 100

    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
    )

    class Meta:
        db_table = 'main_asset_category'


class Asset(AuditEntity):
    MODEL_NUMBER_MAX_LENGTH = 20
    MODEL_NAME_MAX_LENGTH = 100

    model_number = models.CharField(
        max_length=MODEL_NUMBER_MAX_LENGTH,
    )

    model_name = models.CharField(
        max_length=MODEL_NAME_MAX_LENGTH,
    )

    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
    )

    asset_category = models.ForeignKey(
        AssetCategory,
        on_delete=models.CASCADE,
    )


class CustomerAsset(AuditEntity):
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

    class Meta:
        db_table = 'main_customer_asset'
