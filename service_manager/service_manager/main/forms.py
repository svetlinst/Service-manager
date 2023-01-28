from django import forms
from django.core.exceptions import ValidationError

from service_manager.core.forms import BootstrapFormMixin
from service_manager.customers.models import Customer, CustomerAsset, CustomerRepresentative, CustomerDepartment
from service_manager.main.models import ServiceOrderHeader, ServiceOrderDetail, ServiceOrderNote
from django.utils.translation import gettext_lazy as _
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Checkbox


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

    def clean_order_tracking_number(self):
        data = self.cleaned_data['order_tracking_number'].strip().lower()
        service_order = ServiceOrderHeader.objects.filter(slug__exact=data)

        if not service_order:
            raise ValidationError(_(f'Invalid Tracking order number!'))

        return data
