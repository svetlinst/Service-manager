from django.db import models

from service_manager.core.models import BaseAuditEntity


class CustomerType(BaseAuditEntity):
    NAME_MAX_LENGTH = 50

    name = models.CharField(
        max_length=NAME_MAX_LENGTH,
    )

    def __str__(self):
        return self.name


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
