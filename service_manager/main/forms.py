from django import forms

from service_manager.core.forms import BootstrapFormMixin
from service_manager.customers.models import Customer, CustomerAsset, CustomerRepresentative, CustomerDepartment
from service_manager.main.models import ServiceOrderHeader, ServiceOrderDetail, ServiceOrderNote


class CreateServiceOrderHeaderForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = ServiceOrderHeader
        fields = ('customer', 'customer_asset', 'department', 'handed_over_by', 'accepted_by',)

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
        self.fields['accepted_by'].disabled = True


class EditServiceOrderDetailForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = ServiceOrderDetail
        fields = ('material', 'quantity', 'discount')


class CreateServiceOrderDetailForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = ServiceOrderDetail
        fields = ('material', 'quantity', 'discount')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['quantity'].initial = 1
        self.fields['discount'].initial = 0


class CreateServiceOrderNoteForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = ServiceOrderNote
        fields = ('service_order', 'created_by', 'note',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if 'service_order' in self.initial:
            service_order_id = int(self.initial['service_order'])
            self.fields['service_order'].queryset = ServiceOrderHeader.objects.filter(pk=service_order_id)

        self.fields['service_order'].disabled = True
        self.fields['created_by'].disabled = True
