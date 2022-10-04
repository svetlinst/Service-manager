from django import forms

from service_manager.core.forms import BootstrapFormMixin
from service_manager.customers.models import Customer, CustomerAsset, CustomerRepresentative, CustomerDepartment


class EditCustomerForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'


class CreateCustomerForm(EditCustomerForm):
    pass


class CreateCustomerAssetForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['customer'].disabled = True

    class Meta:
        model = CustomerAsset
        fields = ('customer', 'asset', 'serial_number', 'product_number')


class EditCustomerAssetForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = CustomerAsset
        fields = ('serial_number', 'product_number',)


class EditCustomerRepresentativeForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = CustomerRepresentative
        fields = ('first_name', 'last_name', 'email_address', 'phone_number')


class CreateCustomerRepresentativeForm(BootstrapFormMixin, forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['customer'].disabled = True

    class Meta:
        model = CustomerRepresentative
        fields = ('customer', 'first_name', 'last_name', 'email_address', 'phone_number')


class CreateCustomerDepartmentForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = CustomerDepartment
        fields = ('customer', 'name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'customer_id' in self.initial:
            customer_id = int(self.initial['customer_id'])
            self.fields['customer'].queryset = Customer.objects.filter(pk=customer_id)

        self.fields['customer'].disabled = True
