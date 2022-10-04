from django import forms

from service_manager.core.forms import BootstrapFormMixin
from service_manager.master_data.models import Asset, Material, MaterialCategory, Brand, AssetCategory


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


class EditMaterialCategoryForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = MaterialCategory
        fields = '__all__'


class EditBrandForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Brand
        fields = '__all__'


class EditAssetCategoryForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = AssetCategory
        fields = '__all__'
