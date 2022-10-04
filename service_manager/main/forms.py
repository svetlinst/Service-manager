from django import forms

from service_manager.customers.models import Customer, CustomerAsset, CustomerRepresentative, CustomerDepartment
from service_manager.main.models import ServiceOrderHeader, ServiceOrderDetail, ServiceOrderNote


class CreateServiceOrderHeaderForm(forms.ModelForm):
    class Meta:
        model = ServiceOrderHeader
        fields = ('customer', 'customer_asset', 'department', 'handed_over_by',)
        widgets = {
            'customer': forms.Select(
                attrs={'class': 'form-control'},
            ),
            'customer_asset': forms.Select(
                attrs={'class': 'form-control', 'id': 'customer_asset_id'},
            ),
            'department': forms.Select(
                attrs={'class': 'form-control'},
            ),
            'handed_over_by': forms.Select(
                attrs={'class': 'form-control'},
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'customer' in self.initial:
            customer_id = int(self.initial['customer'])
            self.fields['customer'].queryset = Customer.objects.filter(pk=customer_id)
            self.fields['customer_asset'].queryset = CustomerAsset.objects.filter(customer=customer_id)
            self.fields['handed_over_by'].queryset = CustomerRepresentative.objects.filter(
                customer=customer_id)
            self.fields['department'].queryset = CustomerDepartment.objects.filter(customer=customer_id)

        self.fields['customer'].disabled = True
        self.fields['customer_asset'].disabled = True


class EditServiceOrderDetailForm(forms.ModelForm):
    class Meta:
        model = ServiceOrderDetail
        fields = ('service_order', 'material', 'quantity', 'discount')
        widgets = {
            'service_order': forms.HiddenInput(
                attrs={'class': 'form-control'},
            ),
            'material': forms.Select(
                attrs={'class': 'form-control'},
            ),
            'quantity': forms.NumberInput(
                attrs={'class': 'form-control'},
            ),
            'discount': forms.NumberInput(
                attrs={'class': 'form-control'},
            ),
        }


class CreateServiceOrderDetailForm(forms.ModelForm):
    class Meta(EditServiceOrderDetailForm.Meta):
        model = ServiceOrderDetail

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['quantity'].initial = 1
        self.fields['discount'].initial = 0

        if 'service_order' in self.initial:
            service_order_id = int(self.initial['service_order'])
            self.fields['service_order'].queryset = ServiceOrderHeader.objects.filter(pk=service_order_id)


class CreateServiceOrderNoteForm(forms.ModelForm):
    class Meta:
        model = ServiceOrderNote
        fields = ('service_order', 'created_by', 'note',)
        widgets = {
            'service_order': forms.Select(
                attrs={'class': 'form-control'},
            ),
            'note': forms.Textarea(
                attrs={'class': 'form-control'},
            ),
            'created_by': forms.Select(
                attrs={'class': 'form-control'},
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'service_order' in self.initial:
            service_order_id = int(self.initial['service_order'])
            self.fields['service_order'].queryset = ServiceOrderHeader.objects.filter(pk=service_order_id)

        self.fields['service_order'].disabled = True
