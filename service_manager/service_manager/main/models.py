from django.contrib.auth.models import User
from django.db import models

from service_manager.accounts.models import Profile, AppUser
from service_manager.core.models import BaseAuditEntity, ActiveModel
from service_manager.customers.models import Customer, CustomerAsset, CustomerRepresentative, CustomerDepartment
from service_manager.master_data.models import CustomerType, Asset, Material
from django.utils.translation import gettext_lazy as _


class ServiceOrderHeader(ActiveModel, BaseAuditEntity):
    problem_description = models.TextField(
        _('problem_description'),
        null=False,
        blank=False,
    )

    is_serviced = models.BooleanField(
        _('is_serviced'),
        default=False,
    )

    is_completed = models.BooleanField(
        _('is_completed'),
        default=False,
    )

    serviced_on = models.DateTimeField(
        _('serviced_on'),
        null=True,
        blank=True,
    )

    completed_on = models.DateTimeField(
        _('completed_on'),
        null=True,
        blank=True,
    )

    send_emails = models.BooleanField(
        _('send_emails'),
        default=True,
        null=False,
        blank=False,
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        verbose_name=_('customer'),
    )

    customer_asset = models.ForeignKey(
        CustomerAsset,
        on_delete=models.CASCADE,
        verbose_name=_('customer_asset'),
    )

    department = models.ForeignKey(
        CustomerDepartment,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name=_('department'),
    )

    handed_over_by = models.ForeignKey(
        CustomerRepresentative,
        on_delete=models.CASCADE,
        related_name='handed_by_customer_representative',
        null=True,
        blank=True,
        verbose_name=_('handed_over_by'),
    )

    accepted_by = models.ForeignKey(
        AppUser,
        on_delete=models.CASCADE,
        related_name='accepted_by',
        null=True,
        blank=True,
        verbose_name=_('accepted_by'),
    )

    serviced_by = models.ForeignKey(
        AppUser,
        on_delete=models.CASCADE,
        related_name='serviced_by',
        null=True,
        blank=True,
        verbose_name=_('serviced_by'),
    )

    completed_by = models.ForeignKey(
        AppUser,
        on_delete=models.CASCADE,
        related_name='completed_by',
        null=True,
        blank=True,
        verbose_name=_('completed_by'),
    )

    handed_over_to = models.ForeignKey(
        CustomerRepresentative,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='handed_to_customer_representative',
        verbose_name=_('handed_over_to'),
    )

    @property
    def total_amount_due(self):
        return f'{sum([x.total_amount for x in self.serviceorderdetail_set.all()]):.2f}'

    @property
    def status(self):
        if not self.active:
            return 'Deleted'
        if not self.serviced_on:
            return 'New'
        if not self.completed_on:
            return 'Serviced'
        if self.completed_on:
            return 'Completed'

    def __str__(self):
        return f'{str(self.customer)}--{str(self.customer_asset)}'


class ServiceOrderDetail(ActiveModel, BaseAuditEntity):
    quantity = models.FloatField(_('quantity'))
    discount = models.FloatField(_('discount'))

    service_order = models.ForeignKey(
        ServiceOrderHeader,
        on_delete=models.CASCADE,
        verbose_name=_('service_order'),
    )

    material = models.ForeignKey(
        Material,
        on_delete=models.CASCADE,
        verbose_name=_('material'),
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


class ServiceOrderNote(ActiveModel, BaseAuditEntity):
    note = models.TextField(_('note'))

    created_by = models.ForeignKey(
        AppUser,
        on_delete=models.CASCADE,
        verbose_name=_('created_by'),
    )

    service_order = models.ForeignKey(
        ServiceOrderHeader,
        on_delete=models.CASCADE,
        verbose_name=_('service_order'),
    )

    class Meta:
        ordering = ('-created_on',)
