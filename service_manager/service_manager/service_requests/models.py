from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import gettext_lazy as _

from service_manager.core.mixins import PricingMixin
from service_manager.core.models import ActiveModel, BaseAuditEntity
from service_manager.main.models import ServiceRequest
from service_manager.master_data.models import Material


# Create your models here.
class DeliveryRequest(PricingMixin, ActiveModel, BaseAuditEntity):
    quantity = models.FloatField(_('quantity'))

    discount = models.FloatField(
        _('discount'),
        validators=[
            MinValueValidator(0),
        ]
    )

    material = models.ForeignKey(
        Material,
        on_delete=models.CASCADE,
        verbose_name=_('material'),
    )

    service_request = models.ForeignKey(
        ServiceRequest,
        on_delete=models.CASCADE,
        verbose_name=_('service_request'),
        null=False,
        blank=False,
    )
