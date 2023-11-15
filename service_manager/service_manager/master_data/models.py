from django.db import models

from service_manager.core.models import BaseAuditEntity, ActiveModel
from django.utils.translation import gettext_lazy as _


class CustomerType(ActiveModel, BaseAuditEntity):
    NAME_MAX_LENGTH = 50

    name = models.CharField(
        _('name'),
        max_length=NAME_MAX_LENGTH,
    )

    def __str__(self):
        return self.name


class Brand(ActiveModel, BaseAuditEntity):
    NAME_MAX_LENGTH = 100

    name = models.CharField(
        _('name'),
        max_length=NAME_MAX_LENGTH,
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class AssetCategory(ActiveModel, BaseAuditEntity):
    NAME_MAX_LENGTH = 100

    name = models.CharField(
        _('name'),
        max_length=NAME_MAX_LENGTH,
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class Asset(ActiveModel, BaseAuditEntity):
    MODEL_NUMBER_MAX_LENGTH = 20
    MODEL_NAME_MAX_LENGTH = 100

    model_number = models.CharField(
        _('model_number'),
        max_length=MODEL_NUMBER_MAX_LENGTH,
    )

    model_name = models.CharField(
        _('model_name'),
        max_length=MODEL_NAME_MAX_LENGTH,
    )

    brand = models.ForeignKey(
        Brand,
        on_delete=models.CASCADE,
        verbose_name=_('brand'),
    )

    category = models.ForeignKey(
        AssetCategory,
        on_delete=models.CASCADE,
        verbose_name=_('category'),
    )

    def __str__(self):
        return f'{self.brand} {self.model_name} {self.model_number} ({self.category})'


class MaterialCategory(ActiveModel, BaseAuditEntity):
    NAME_MAX_LENGTH = 20

    name = models.CharField(
        _('name'),
        max_length=NAME_MAX_LENGTH,
    )

    def __str__(self):
        return self.name


class Material(ActiveModel, BaseAuditEntity):
    NAME_MAX_LENGTH = 100
    VAT_PCT = .2

    name = models.CharField(
        _('name'),
        max_length=NAME_MAX_LENGTH,
    )

    price = models.FloatField(verbose_name=_('price'))

    category = models.ForeignKey(
        MaterialCategory,
        on_delete=models.CASCADE,
        verbose_name=_('category'),
    )

    @property
    def price_no_vat(self):
        return self.price / (1 + self.VAT_PCT)

    def __str__(self):
        return f'{self.name} ({str(self.category)})'


class SLA(ActiveModel, BaseAuditEntity):
    NAME_MAX_LENGTH = 256
    DESCRIPTION_MAX_LENGTH = 1024

    name = models.CharField(
        _('name'),
        max_length=NAME_MAX_LENGTH,
        null=False,
        blank=False,
    )

    description = models.CharField(
        _('description'),
        max_length=DESCRIPTION_MAX_LENGTH,
        null=True,
        blank=True,
    )

    def __str__(self):
        if self.description:
            return f'{self.name} ({self.description})'
        return self.name

