import django.views.generic as views
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth import mixins as auth_mixins

from service_manager.customers.forms import EditCustomerForm, CreateCustomerForm, CreateCustomerAssetForm, \
    EditCustomerAssetForm, CreateCustomerRepresentativeForm, EditCustomerRepresentativeForm, \
    CreateCustomerDepartmentForm
from service_manager.customers.models import Customer, CustomerAsset, CustomerRepresentative, CustomerDepartment


class CustomersListView(auth_mixins.LoginRequiredMixin, views.ListView):
    model = Customer
    template_name = 'customer/customers.html'
    ordering = ('name',)

    def get_queryset(self):
        queryset = super().get_queryset()

        search_text = self.request.GET.get('search_value', None)
        if search_text:
            queryset = queryset.filter(Q(name__icontains=search_text) | Q(vat__icontains=search_text))
        return queryset


class CustomerDetailView(auth_mixins.LoginRequiredMixin, views.DetailView):
    model = Customer
    template_name = 'customer/customer_detail.html'


class EditCustomerView(auth_mixins.LoginRequiredMixin, views.UpdateView):
    model = Customer
    form_class = EditCustomerForm
    template_name = 'customer/customer_edit.html'

    def get_success_url(self):
        return reverse_lazy('customer_detail', kwargs={'pk': self.kwargs['pk']})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = context['customer']

        context['customer_assets'] = customer.customerasset_set.all()
        context['customer_representatives'] = customer.customerrepresentative_set.all()
        context['customer_departments'] = customer.customerdepartment_set.all()

        search_text = self.request.GET.get('search_value', None)
        if search_text:
            context['customer_assets'] = customer.customerasset_set.filter(serial_number__icontains=search_text)

        representative_search = self.request.GET.get('representative', None)
        if representative_search:
            context['customer_representatives'] = customer.customerrepresentative_set.filter(
                Q(first_name__icontains=representative_search) | Q(last_name__icontains=representative_search))

        department_search = self.request.GET.get('departments', None)
        if department_search:
            context['customer_departments'] = customer.customerdepartment_set.filter(name__icontains=department_search)

        return context


class CreateCustomerView(auth_mixins.LoginRequiredMixin, views.CreateView):
    model = Customer
    form_class = CreateCustomerForm
    template_name = 'customer/customer_create.html'
    success_url = reverse_lazy('customers_list')


class DeleteCustomerView(auth_mixins.LoginRequiredMixin, views.DeleteView):
    model = Customer
    template_name = 'customer/customer_delete.html'
    success_url = reverse_lazy('customers_list')


class CreateCustomerAssetView(auth_mixins.LoginRequiredMixin, views.CreateView):
    model = CustomerAsset
    form_class = CreateCustomerAssetForm
    template_name = 'customer_asset/customer_asset_create.html'

    def get_success_url(self):
        return reverse_lazy('edit_customer', kwargs={'pk': self.object.customer.pk})

    def get_initial(self):
        customer_id = self.kwargs['customer_id']
        if customer_id:
            self.initial.update({
                'customer': customer_id,
            })
        return super().get_initial()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        customer_id = self.kwargs['customer_id']
        if customer_id:
            customer = Customer.objects.prefetch_related('customerasset_set').filter(pk=customer_id).get()
            context['customer'] = customer
        return context


class EditCustomerAssetView(auth_mixins.LoginRequiredMixin, views.UpdateView):
    model = CustomerAsset
    form_class = EditCustomerAssetForm
    template_name = 'customer_asset/customer_asset_edit.html'

    def get_success_url(self):
        return reverse_lazy('edit_customer', kwargs={'pk': self.object.customer.pk})


class DeleteCustomerAssetView(auth_mixins.LoginRequiredMixin, views.DeleteView):
    model = CustomerAsset
    template_name = 'customer_asset/customer_asset_delete.html'

    def get_success_url(self):
        return reverse_lazy('edit_customer', kwargs={'pk': self.object.customer.pk})


class CustomerRepresentativesListView(auth_mixins.LoginRequiredMixin, views.ListView):
    model = CustomerRepresentative
    template_name = 'customer_representatives/customer_representatives.html'
    ordering = ('first_name', 'last_name')


class CreateCustomerRepresentativeView(auth_mixins.LoginRequiredMixin, views.CreateView):
    model = CustomerRepresentative
    template_name = 'customer_representatives/customer_representatives_create.html'
    form_class = CreateCustomerRepresentativeForm

    def get_initial(self):
        customer_id = self.kwargs['customer_id']
        if customer_id:
            self.initial.update({
                'customer': customer_id,
            })
        return super().get_initial()

    def get_success_url(self):
        return reverse_lazy('edit_customer', kwargs={'pk': self.object.customer.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        customer_id = self.kwargs['customer_id']
        if customer_id:
            customer = Customer.objects.prefetch_related('customerrepresentative_set').filter(pk=customer_id).get()
            context['customer'] = customer
        return context


class EditCustomerRepresentativeView(auth_mixins.LoginRequiredMixin, views.UpdateView):
    model = CustomerRepresentative
    template_name = 'customer_representatives/customer_representative_edit.html'
    form_class = EditCustomerRepresentativeForm

    def get_success_url(self):
        return reverse_lazy('edit_customer', kwargs={'pk': self.object.customer.pk})


class DeleteCustomerRepresentativeView(auth_mixins.LoginRequiredMixin, views.DeleteView):
    model = CustomerRepresentative
    template_name = 'customer_representatives/customer_representative_delete.html'

    def get_success_url(self):
        return reverse_lazy('edit_customer', kwargs={'pk': self.object.customer.pk})


class CustomerDepartmentsListView(auth_mixins.LoginRequiredMixin, views.ListView):
    model = CustomerDepartment
    template_name = 'customer_department/customer_departments.html'


class CreateCustomerDepartmentView(auth_mixins.LoginRequiredMixin, views.CreateView):
    model = CustomerDepartment
    template_name = 'customer_department/customer_department_create.html'
    form_class = CreateCustomerDepartmentForm

    def get_initial(self):
        customer_id = self.kwargs['customer_id']

        if customer_id:
            self.initial.update({
                'customer': customer_id,
            })

        return super().get_initial()

    def get_success_url(self):
        customer_id = self.kwargs['customer_id']
        if customer_id:
            return reverse_lazy('edit_customer', kwargs={'pk': customer_id})
        return reverse_lazy('customers_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        customer_id = self.kwargs['customer_id']
        if customer_id:
            customer = Customer.objects.prefetch_related('customerdepartment_set').filter(pk=customer_id).get()
            context['customer'] = customer
        return context


class EditCustomerDepartmentView(auth_mixins.LoginRequiredMixin, views.UpdateView):
    model = CustomerDepartment
    template_name = 'customer_department/customer_department_edit.html'
    form_class = CreateCustomerDepartmentForm

    def get_success_url(self):
        customer_id = self.kwargs['customer_id']
        if customer_id:
            return reverse_lazy('edit_customer', kwargs={'pk': customer_id})
        return reverse_lazy('customers_list')


class DeleteCustomerDepartmentView(auth_mixins.LoginRequiredMixin, views.DeleteView):
    model = CustomerDepartment
    template_name = 'customer_department/customer_department_delete.html'

    def get_success_url(self):
        customer_id = self.kwargs['customer_id']
        if customer_id:
            return reverse_lazy('edit_customer', kwargs={'pk': customer_id})
        return reverse_lazy('customers_list')
