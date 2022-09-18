from django import forms

from service_manager.main.models import Customer, Asset, Material, CustomerAsset, ServiceOrderHeader, \
    CustomerRepresentative, ServiceOrderDetail


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


class CreateCustomerAssetForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['customer'].disabled = True

    class Meta:
        model = CustomerAsset
        fields = ('customer', 'asset', 'serial_number', 'product_number')
        widgets = {
            'customer': forms.Select(
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


class CreateServiceOrderHeaderForm(forms.ModelForm):
    class Meta:
        model = ServiceOrderHeader
        fields = ('customer', 'customer_asset', 'customer_representative',)
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
            'customer_representative': forms.Select(
                attrs={'class': 'form-control'},
            ),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'customer' in self.initial:
            customer_id = int(self.initial['customer'])
            self.fields['customer'].queryset = Customer.objects.filter(pk=customer_id)
            self.fields['customer_asset'].queryset = CustomerAsset.objects.filter(customer=customer_id)
            self.fields['customer_representative'].queryset = CustomerRepresentative.objects.filter(customer=customer_id)

        self.fields['customer'].disabled = True
        self.fields['customer_asset'].disabled = True


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
            'customer': forms.Select(
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


class CreateServiceOrderDetailForm(forms.ModelForm):
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'service_order' in self.initial:
            service_order_id = int(self.initial['service_order'])
            self.fields['service_order'].queryset = ServiceOrderHeader.objects.filter(pk=service_order_id)




