from django import forms

from service_manager.customers.models import Customer, CustomerAsset, CustomerRepresentative, CustomerDepartment


class EditCustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'type': forms.Select(
                attrs={'class': 'form-control'},
            ),
            'vat': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'email_address': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'phone_number': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
        }


class CreateCustomerForm(EditCustomerForm):
    pass


class CreateCustomerAssetForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['customer'].disabled = True

    class Meta:
        model = CustomerAsset
        fields = ('customer', 'asset', 'serial_number', 'product_number')
        widgets = {
            'customer': forms.HiddenInput(
                attrs={'class': 'form-control'},
            ),
            'asset': forms.Select(
                attrs={'class': 'form-control'},
            ),
            'serial_number': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'product_number': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
        }


class EditCustomerAssetForm(forms.ModelForm):
    class Meta:
        model = CustomerAsset
        fields = ('serial_number', 'product_number',)
        widgets = {
            'serial_number': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'product_number': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
        }


class EditCustomerRepresentativeForm(forms.ModelForm):
    class Meta:
        model = CustomerRepresentative
        fields = ('first_name', 'last_name', 'email_address', 'phone_number')
        widgets = {
            'first_name': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'last_name': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'email_address': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'phone_number': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
        }


class CreateCustomerRepresentativeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['customer'].disabled = True

    class Meta:
        model = CustomerRepresentative
        fields = ('customer', 'first_name', 'last_name', 'email_address', 'phone_number')
        widgets = {
            'customer': forms.HiddenInput(
                attrs={'class': 'form-control'},
            ),
            'first_name': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'last_name': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'email_address': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'phone_number': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
        }


class CreateCustomerDepartmentForm(forms.ModelForm):
    class Meta:
        model = CustomerDepartment
        fields = ('customer', 'name',)
        widgets = {
            'customer': forms.HiddenInput(
                attrs={'class': 'form-control'},
            ),
            'name': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'customer_id' in self.initial:
            customer_id = int(self.initial['customer_id'])
            self.fields['customer'].queryset = Customer.objects.filter(pk=customer_id)

        self.fields['customer'].disabled = True
