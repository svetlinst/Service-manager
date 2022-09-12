from django import forms

from service_manager.main.models import Customer


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



