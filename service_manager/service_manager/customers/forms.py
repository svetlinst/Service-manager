from django import forms

from service_manager.core.forms import BootstrapFormMixin
from service_manager.customers.models import Customer, CustomerAsset, CustomerRepresentative, CustomerDepartment
from service_manager.master_data.models import Asset


class EditCustomerForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Customer
        fields = ('type', 'name', 'vat', 'email_address', 'phone_number', 'has_subscription', 'is_regular_customer',)

        widgets = {
            'has_subscription': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                },
            ),
            'is_regular_customer': forms.CheckboxInput(
                attrs={
                    'class': 'form-check-input',
                },
            ),
        }


class CreateCustomerForm(EditCustomerForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['has_subscription'].initial = False
        self.fields['is_regular_customer'].initial = False


class CreateCustomerAssetForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['asset'].queryset = Asset.objects.all()
        pass

    class Meta:
        model = CustomerAsset
        fields = ('asset', 'serial_number', 'product_number', 'inventory_number')


class EditCustomerAssetForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = CustomerAsset
        fields = ('serial_number', 'product_number', 'inventory_number')


class EditCustomerRepresentativeForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = CustomerRepresentative
        fields = ('first_name', 'last_name', 'email_address', 'phone_number')


class CreateCustomerRepresentativeForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = CustomerRepresentative
        fields = ('first_name', 'last_name', 'email_address', 'phone_number')


class CreateCustomerDepartmentForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = CustomerDepartment
        fields = ('name',)
