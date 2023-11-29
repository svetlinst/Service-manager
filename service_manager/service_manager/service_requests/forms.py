from django import forms
from django.db.models import Q

from service_manager.core.forms import BootstrapFormMixin
from service_manager.master_data.models import Material
from service_manager.service_requests.models import DeliveryRequest


class CreateDeliveryRequestForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = DeliveryRequest
        fields = ('material', 'quantity', 'discount')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['quantity'].initial = 1
        self.fields['discount'].initial = 0
        queryset = Material.objects.all()

        category = self.initial.get('category' or None)
        if category:
            queryset = queryset.filter(category=category)

        search = self.initial.get('search' or None)
        if search:
            queryset = queryset.filter(Q(name__icontains=search) | Q(category__name__icontains=search))

        self.fields['material'].queryset = queryset

class EditDeliveryRequestForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = DeliveryRequest
        fields = ('material', 'quantity', 'discount')