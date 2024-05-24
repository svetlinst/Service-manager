from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db import models

from service_manager.accounts.models import Profile, AppUser
from service_manager.core.mixins import PricingMixin
from service_manager.core.models import BaseAuditEntity, ActiveModel
from service_manager.customers.models import Customer, CustomerAsset, CustomerRepresentative, CustomerDepartment
from service_manager.customers.validators import phone_number_validator
from service_manager.master_data.models import CustomerType, Asset, Material, SLA
from django.utils.translation import gettext_lazy as _


class ServiceOrderHeader(ActiveModel, BaseAuditEntity):
    TYPE_CHOICE_CUSTOMER_OFFICE = _('Customer office')
    TYPE_CHOICE_BROUGHT_IN = _('Brought in')

    TYPE_CHOICES = (
        (TYPE_CHOICE_CUSTOMER_OFFICE, _('Customer office')),
        (TYPE_CHOICE_BROUGHT_IN, _('Brought in')),
    )

    problem_description = models.TextField(
        _('problem description'),
        null=False,
        blank=False,
    )

    is_serviced = models.BooleanField(
        _('is serviced'),
        default=False,
    )

    is_completed = models.BooleanField(
        _('is completed'),
        default=False,
    )

    serviced_on = models.DateTimeField(
        _('serviced on'),
        null=True,
        blank=True,
    )

    completed_on = models.DateTimeField(
        _('completed on'),
        null=True,
        blank=True,
    )

    send_emails = models.BooleanField(
        _('send emails'),
        default=False,
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
        verbose_name=_('customer asset'),
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
        verbose_name=_('handed over by'),
    )

    accepted_by = models.ForeignKey(
        AppUser,
        on_delete=models.CASCADE,
        related_name='accepted_by',
        null=True,
        blank=True,
        verbose_name=_('accepted by'),
    )

    serviced_by = models.ForeignKey(
        AppUser,
        on_delete=models.CASCADE,
        related_name='serviced_by',
        null=True,
        blank=True,
        verbose_name=_('serviced by'),
    )

    completed_by = models.ForeignKey(
        AppUser,
        on_delete=models.CASCADE,
        related_name='completed_by',
        null=True,
        blank=True,
        verbose_name=_('completed by'),
    )

    handed_over_to = models.ForeignKey(
        CustomerRepresentative,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='handed_to_customer_representative',
        verbose_name=_('handed over to'),
    )

    packaging = models.CharField(
        _('packaging'),
        max_length=256,
        null=True,
        blank=True,
    )

    place_of_service = models.CharField(
        _('place of service'),
        max_length=20,
        null=False,
        blank=False,
        default=TYPE_CHOICE_BROUGHT_IN,
        choices=TYPE_CHOICES,
    )

    service_level_agreement = models.ForeignKey(
        SLA,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='service_level_agreement',
        verbose_name=_('service_level_agreement'),
    )

    slug = models.SlugField(
        null=True,
        blank=True,
    )

    @property
    def total_amount_due(self):
        return f'{sum([x.total_amount for x in self.serviceorderdetail_set.all()]):.2f}'

    @property
    def status(self):
        if not self.active:
            return _('Deleted')
        if not self.serviced_on:
            return _('New')
        if not self.completed_on:
            return _('Serviced')
        if self.completed_on:
            return _('Completed')

    def __str__(self):
        return f'{str(self.customer)}--{str(self.customer_asset)}'


class ServiceOrderDetail(PricingMixin, ActiveModel, BaseAuditEntity):
    quantity = models.FloatField(_('quantity'))
    discount = models.FloatField(
        _('discount'),
        validators=[
            MinValueValidator(0),
        ]
    )

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


class CustomerNotification(ActiveModel, BaseAuditEntity):
    COMMENT_MAX_LENGTH = 100
    TYPE_CHOICE_PHONE = 1
    TYPE_CHOICE_EMAIL = 2

    TYPE_CHOICES = (
        (TYPE_CHOICE_PHONE, _('By phone')),
        (TYPE_CHOICE_EMAIL, _('By email')),
    )

    notified_on = models.DateTimeField(
        verbose_name=_('notified_on'),
        blank=False,
        null=False,
    )

    notified_by = models.ForeignKey(
        AppUser,
        on_delete=models.CASCADE,
        verbose_name=_('created_by'),
    )

    notification_method = models.CharField(
        verbose_name=_('notification_method'),
        max_length=2,
        null=False,
        blank=False,
        choices=TYPE_CHOICES,
        default=TYPE_CHOICE_PHONE,
    )

    comment = models.CharField(
        verbose_name=_('comment'),
        max_length=COMMENT_MAX_LENGTH,
        null=True,
        blank=False,
    )

    service_order_current_status = models.CharField(
        verbose_name=_('service_order_current_status'),
        max_length=20,
        blank=False,
        null=False,
    )

    service_order = models.ForeignKey(
        ServiceOrderHeader,
        on_delete=models.CASCADE,
        verbose_name=_('service_order'),
    )

    class Meta:
        ordering = ('-created_on',)


class ServiceRequest(ActiveModel, BaseAuditEntity):
    PROBLEM_DESCRIPTION_MAX_LENGTH = 255
    REQUESTOR_NAME_MAX_LENGTH = 100
    REQUESTOR_PHONE_NUMBER_MAX_LENGTH = 20
    RESOLUTION_MAX_LENGTH = 100
    ORDER_TYPE_MAX_LENGTH = 1

    TYPE_NEW = '1'
    TYPE_IN_PROGRESS = '2'
    TYPE_RESOLVED = '3'
    TYPE_CLOSED = '4'
    TYPE_REJECTED = '5'

    ORDER_TYPE_SERVICE = 1
    ORDER_TYPE_DELIVERY = 2

    TYPE_CHOICES = (
        (TYPE_NEW, _('New')),
        (TYPE_IN_PROGRESS, _('In progress')),
        (TYPE_RESOLVED, _('Resolved')),
        (TYPE_CLOSED, _('Closed')),
        (TYPE_REJECTED, _('Rejected')),
    )

    ORDER_TYPE_CHOICES = (
        (ORDER_TYPE_SERVICE, _('Service')),
        (ORDER_TYPE_DELIVERY, _('Delivery'))
    )

    problem_description = models.CharField(
        verbose_name=_('problem description'),
        max_length=PROBLEM_DESCRIPTION_MAX_LENGTH,
        null=False,
        blank=False,
    )

    requestor_name = models.CharField(
        verbose_name=_('requestor name'),
        max_length=REQUESTOR_NAME_MAX_LENGTH,
        null=False,
        blank=False,
    )

    requestor_phone_number = models.CharField(
        verbose_name=_('requestor phone number'),
        max_length=REQUESTOR_PHONE_NUMBER_MAX_LENGTH,
        null=False,
        blank=False,
        validators=(
            phone_number_validator,
        ),
    )

    resolution = models.CharField(
        verbose_name=_('resolution'),
        max_length=RESOLUTION_MAX_LENGTH,
        null=True,
        blank=True,
    )

    status = models.CharField(
        verbose_name=_('status'),
        max_length=1,
        choices=TYPE_CHOICES,
        default=TYPE_NEW,
        null=False,
        blank=False,
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        verbose_name=_('customer'),
    )

    accepted_by = models.ForeignKey(
        AppUser,
        on_delete=models.CASCADE,
        related_name='request_accepted_by',
        null=True,
        blank=True,
        verbose_name=_('accepted by'),
    )

    handled_by = models.ForeignKey(
        AppUser,
        on_delete=models.CASCADE,
        related_name='handled_by',
        null=True,
        blank=True,
        verbose_name=_('handled by'),
    )

    handled_on = models.DateTimeField(
        verbose_name=_('handled on'),
        blank=True,
        null=True,
    )

    closed_by = models.ForeignKey(
        AppUser,
        on_delete=models.CASCADE,
        related_name='closed_by',
        null=True,
        blank=True,
        verbose_name=_('closed by'),
    )

    closed_on = models.DateTimeField(
        verbose_name=_('closed on'),
        blank=True,
        null=True,
    )

    service_order = models.ForeignKey(
        ServiceOrderHeader,
        on_delete=models.CASCADE,
        verbose_name=_('service order'),
        null=True,
        blank=True,
    )

    order_type = models.IntegerField(
        verbose_name=_('order type'),
        choices=ORDER_TYPE_CHOICES,
        default=ORDER_TYPE_SERVICE,
        null=False,
        blank=False,
    )

    def is_open(self):
        if self.status in [str(k) for k, v in self.TYPE_CHOICES if int(k) < 4]:
            return True
        return False

    def is_rejected(self):
        if self.status == str(self.TYPE_REJECTED):
            return True
        return False

    def is_finalized(self):
        if self.status == str(self.TYPE_CLOSED):
            return True
        return False

    def is_handled(self):
        if self.status < str(self.TYPE_RESOLVED):
            return False
        return True

    @property
    def total_amount_due(self):
        return f'{sum([x.total_amount for x in self.deliveryrequest_set.all()]):.2f}'

    class Meta:
        ordering = ('status', '-created_on',)
