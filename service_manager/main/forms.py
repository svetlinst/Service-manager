from django import forms

from service_manager.core.forms import BootstrapFormMixin
from service_manager.customers.models import Customer, CustomerAsset, CustomerRepresentative, CustomerDepartment
from service_manager.main.models import ServiceOrderHeader, ServiceOrderDetail, ServiceOrderNote


class CreateServiceOrderHeaderForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = ServiceOrderHeader
        fields = ('department', 'handed_over_by', 'send_emails', 'problem_description',)

        widgets = {
            'send_emails': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
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
