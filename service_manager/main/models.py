from django.contrib.auth.models import User
from django.core.validators import EmailValidator
from django.db import models


class BaseAuditEntity(models.Model):
    created_on = models.DateTimeField(
        auto_now_add=True,
    )

    updated_on = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        abstract = True


class CustomerType(BaseAuditEntity):
    NAME_MAX_LENGTH = 50

    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'main_customer_type'


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
        )
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
        db_table = 'main_customer_representative'
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
        db_table = 'main_customer_department'
        ordering = ('name',)


class Brand(BaseAuditEntity):
    NAME_MAX_LENGTH = 100

    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class AssetCategory(BaseAuditEntity):
    NAME_MAX_LENGTH = 100

    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'main_asset_category'
        ordering = ('name',)


class Asset(BaseAuditEntity):
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

    category = models.ForeignKey(
        AssetCategory,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.category}---{self.brand.name}---{self.model_number}---{self.model_name}'



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
        db_table = 'main_customer_asset'
        ordering = ('asset__category__name', 'asset__brand__name', 'asset__model_name', 'serial_number',)


class Role(BaseAuditEntity):
    NAME_MAX_LENGTH = 20

    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
    )

    def __str__(self):
        return self.name


class Employee(BaseAuditEntity):
    role = models.ManyToManyField(
        Role,
    )

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=False,
    )

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'


class MaterialCategory(BaseAuditEntity):
    NAME_MAX_LENGTH = 20

    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
    )

    def __str__(self):
        return self.name


class Material(BaseAuditEntity):
    NAME_MAX_LENGTH = 100

    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
    )

    price = models.FloatField()

    category = models.ForeignKey(
        MaterialCategory,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{self.name} ({str(self.category)})'


class ServiceOrderHeader(BaseAuditEntity):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
    )

    customer_asset = models.ForeignKey(
        CustomerAsset,
        on_delete=models.CASCADE,
    )

    customer_representative = models.ForeignKey(
        CustomerRepresentative,
        on_delete=models.CASCADE,
    )

    department = models.ForeignKey(
        CustomerDepartment,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )

    is_serviced = models.BooleanField(
        default=False,
    )

    is_completed = models.BooleanField(
        default=False,
    )

    serviced_by = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='serviced_by',
        null=True,
        blank=True
    )

    serviced_on = models.DateTimeField(
        null=True,
        blank=True,
    )

    completed_on = models.DateTimeField(
        null=True,
        blank=True,
    )

    completed_by = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name='completed_by',
        null=True,
        blank=True,
    )

    @property
    def total_amount_due(self):
        return f'{sum([x.total_amount for x in self.serviceorderdetail_set.all()]):.2f}'

    def __str__(self):
        return f'{str(self.customer)}--{str(self.customer_asset)}'

    class Meta:
        db_table = 'main_service_order_header'


class ServiceOrderDetail(BaseAuditEntity):
    quantity = models.FloatField()
    discount = models.FloatField()

    service_order = models.ForeignKey(
        ServiceOrderHeader,
        on_delete=models.CASCADE,
    )

    material = models.ForeignKey(
        Material,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f'{str(self.service_order)}---{str(self.material)}'

    @property
    def discount_percentage(self):
        pct = 0
        if self.discount > 0:
            pct = self.discount / 100
        return pct

    @property
    def discounted_price(self):
        price = self.material.price
        if self.discount_percentage > 0:
            price = price * (1 - self.discount_percentage)
        return price

    @property
    def total_amount(self):
        return self.discounted_price * self.quantity

    class Meta:
        db_table = 'main_service_order_detail'


class ServiceOrderNote(BaseAuditEntity):
    note = models.TextField()

    created_by = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
    )

    service_order = models.ForeignKey(
        ServiceOrderHeader,
        on_delete=models.CASCADE,
    )

    class Meta:
        ordering = ('-created_on',)
