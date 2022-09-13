from django import forms

from service_manager.main.models import Customer, Asset, Material


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


class CreateAssetForm(forms.ModelForm):
    class Meta:
        model = Asset
        fields = '__all__'
        widgets = {
            'model_name': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'model_number': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'brand': forms.Select(
                attrs={'class': 'form-control'},
            ),
            'category': forms.Select(
                attrs={'class': 'form-control'},
            ),
        }


class EditAssetForm(CreateAssetForm):
    pass


class CreateMaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'category': forms.Select(
                attrs={'class': 'form-control'},
            ),
            'price': forms.NumberInput(
                attrs={'class': 'form-control'},
            ),
        }


class EditMaterialForm(CreateMaterialForm):
    pass
