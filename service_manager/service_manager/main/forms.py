from django import forms
from django.core.exceptions import ValidationError
from django.db.models import Q

from service_manager.core.forms import BootstrapFormMixin
from service_manager.customers.models import Customer, CustomerAsset, CustomerRepresentative, CustomerDepartment
from service_manager.main.models import ServiceOrderHeader, ServiceOrderDetail, ServiceOrderNote, CustomerNotification, \
    ServiceRequest
from django.utils.translation import gettext_lazy as _
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox

from service_manager.master_data.models import Material


class CreateServiceOrderHeaderForm(forms.ModelForm):
    class Meta:
        model = ServiceOrderHeader
        fields = ('department', 'handed_over_by', 'send_emails', 'problem_description', 'packaging', 'place_of_service',
                  'service_level_agreement')

        widgets = {
            'department': forms.Select(
                attrs={
                    'class': 'form-control',
                },
            ),
            'handed_over_by': forms.Select(
                attrs={
                    'class': 'form-control',
                },
            ),
            'problem_description': forms.Textarea(
                attrs={
                    'class': 'form-control',
                },
            ),
            'packaging': forms.TextInput(
                attrs={
                    'class': 'form-control',
                },
            ),
            'send_emails': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                },
            ),
            'place_of_service': forms.RadioSelect(),
            'service_level_agreement': forms.Select(
                attrs={
                    'class': 'form-control',
                },
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'customer' in self.initial:
            customer_id = int(self.initial['customer'])
            self.fields['handed_over_by'].queryset = CustomerRepresentative.objects.filter(
                customer=customer_id)
            self.fields['department'].queryset = CustomerDepartment.objects.filter(customer=customer_id)


class EditServiceOrderDetailForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = ServiceOrderDetail
        fields = ('material', 'quantity', 'discount')


class CreateServiceOrderDetailForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = ServiceOrderDetail
        fields = ('material', 'quantity', 'discount')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['quantity'].initial = 1
        self.fields['discount'].initial = 0
        queryset = Material.objects.all()

        category = self.initial.get('category' or None)
        if category:
            queryset = queryset.filter(category=category)

        search = self.initial.get('search' or None)
        if search:
            queryset = queryset.filter(Q(name__icontains=search) | Q(category__name__icontains=search))

        self.fields['material'].queryset = queryset


class CreateServiceOrderNoteForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = ServiceOrderNote
        fields = ('note',)


class HandoverServiceOrderForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = ServiceOrderHeader
        fields = ('handed_over_to',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        service_order_id = self.initial['service_order']
        service_order_header = ServiceOrderHeader.objects.get(pk=service_order_id)
        representatives = CustomerRepresentative.objects.filter(customer_id=service_order_header.customer_id)
        self.fields['handed_over_to'].queryset = representatives


class ContactForm(BootstrapFormMixin, forms.Form):
    first_name = forms.CharField(max_length=20)
    last_name = forms.CharField(max_length=20)
    email_address = forms.EmailField(max_length=200)
    message = forms.CharField(widget=forms.Textarea, max_length=2000)
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())


class TrackOrderSearchForm(forms.Form):
    order_tracking_number = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            },
        ),
    )

    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox())


class CreateCustomerNotificationForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = CustomerNotification
        fields = ('notified_on', 'comment',)

        widgets = {
            'notified_on': forms.DateTimeInput(
                attrs={
                    'id': 'datetimepicker1Input',
                },
            ),
        }


class CreateServiceRequestForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ('customer', 'requestor_name', 'requestor_phone_number', 'problem_description')

        widgets = {
            'problem_description': forms.Textarea(
                {
                    'rows': 5
                }
            ),
        }


class ServiceRequestAssignHandlerForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ('handled_by',)


class ServiceRequestUpdateResolutionForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = ServiceRequest
        fields = ('resolution',)

        widgets = {
            'resolution': forms.Textarea(
                {
                    'rows': 5
                }
            ),
        }


class ServiceRequestFilteringForm(BootstrapFormMixin, forms.Form):
    status_choices = ServiceRequest.TYPE_CHOICES
    period_choices = [
        (0, _('Today')), (1, _('This week')), (2, _('Last week')),
        (3, _('This month')), (4, _('Last month')), (5, _('Older')),
    ]

    status = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(attrs={'onchange': 'filter_form.submit();'}),
        choices=status_choices,
    )

    search = forms.CharField(
        label=_('Search'),
        required=False,
        widget=forms.TextInput(),
    )

    period = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple(attrs={'onchange': 'filter_form.submit();'}),
        choices=period_choices,
    )
