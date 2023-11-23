from django import forms
from django.utils.translation import gettext_lazy as _

from service_manager.core.forms import BootstrapFormMixin
from service_manager.master_data.models import Asset, Material, MaterialCategory, Brand, AssetCategory, SLA


class CreateAssetForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = AssetCategory.objects.all()

    class Meta:
        model = Asset
        fields = ('category', 'brand', 'model_name', 'model_number')
        widgets = {
            'model_name': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'model_number': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'brand': forms.Select(
                attrs={'class': 'form-select'},
            ),
            'category': forms.Select(
                attrs={'class': 'form-select'},
            ),
        }


class EditAssetForm(CreateAssetForm):
    pass


class CreateMaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ('category', 'name', 'price',)
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control'},
            ),
            'category': forms.Select(
                attrs={'class': 'form-select'},
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
        fields = ('name',)


class EditBrandForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Brand
        fields = ('name',)


class EditAssetCategoryForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = AssetCategory
        fields = ('name',)


class EditSlaForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = SLA
        fields = ('name', 'description')


class CreateSlaForm(EditSlaForm):
    pass


class FilterAssetsForm(BootstrapFormMixin, forms.ModelForm):
    search = forms.CharField(
        label=_('Search'),
        required=False,
        widget=forms.TextInput(attrs={'placeholder': _('brand, model name and number'), }),
    )

    class Meta:
        model = Asset
        fields = ('category',)

    category = forms.ModelChoiceField(
        label=_('Asset Category'),
        required=False,
        queryset=AssetCategory.objects.all(),
        widget=forms.Select(attrs={
            'class': 'form-control',
            'onchange': 'filter_form.submit();',
        }),
    )
