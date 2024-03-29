import django.views.generic as views
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib.auth import mixins as auth_mixins

from service_manager.customers.forms import EditCustomerForm, CreateCustomerForm, CreateCustomerAssetForm, \
    EditCustomerAssetForm, CreateCustomerRepresentativeForm, EditCustomerRepresentativeForm, \
    CreateCustomerDepartmentForm
from service_manager.customers.models import Customer, CustomerAsset, CustomerRepresentative, CustomerDepartment
from service_manager.customers.utils import get_assets_currently_in_service
from service_manager.main.models import ServiceOrderHeader
from service_manager.master_data.models import AssetCategory, Brand, Asset


class CustomersListView(auth_mixins.PermissionRequiredMixin, views.ListView):
    model = Customer
    template_name = 'customer/customers.html'
    paginate_by = 12

    permission_required = 'customers.view_customer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        request = self.request.GET.copy()
        params = request.pop('page', True) and request.urlencode()
        context['params'] = params

        return context

    def get_queryset(self):
        queryset = super().get_queryset().prefetch_related('customerasset_set')

        search_text = self.request.GET.get('search_value', None)
        if search_text:
            cond = (
                    Q(name__icontains=search_text) |
                    Q(vat__icontains=search_text) |
                    Q(email_address__icontains=search_text) |
                    Q(phone_number__icontains=search_text) |
                    Q(customerasset__serial_number__icontains=search_text)
            )
            queryset = queryset.filter(cond).distinct()
        return queryset


class CustomerDetailView(auth_mixins.PermissionRequiredMixin, views.DetailView):
    model = Customer
    template_name = 'customer/customer_detail.html'

    permission_required = 'customers.view_customer'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        customer = context['customer']

        context['customer_assets'] = customer.customerasset_set.all()
        context['customer_representatives'] = customer.customerrepresentative_set.all()
        context['customer_departments'] = customer.customerdepartment_set.all()
        context['customer_service_requests'] = customer.servicerequest_set.all()

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

        service_requests_search = self.request.GET.get('service_requests', None)
        if service_requests_search:
            context['customer_service_requests'] = customer.servicerequest_set.filter(
                problem_description__icontains=service_requests_search)

        assets_being_serviced = get_assets_currently_in_service(customer)

        context['assets_being_serviced'] = assets_being_serviced

        return context


class EditCustomerView(auth_mixins.PermissionRequiredMixin, views.UpdateView):
    model = Customer
    form_class = EditCustomerForm
    template_name = 'customer/customer_edit.html'

    permission_required = ('customers.view_customer', 'customers.change_customer')

    def get_success_url(self):
        return reverse_lazy('customer_detail', kwargs={'pk': self.kwargs['pk']})


class CreateCustomerView(auth_mixins.PermissionRequiredMixin, views.CreateView):
    model = Customer
    form_class = CreateCustomerForm
    template_name = 'customer/customer_create.html'
    success_url = reverse_lazy('customers_list')
    permission_required = 'customers.add_customer'

    def form_valid(self, form):
        customer = form.save(commit=False)
        customer.save()
        self.create_representative_if_individual(customer)
        return super().form_valid(form)

    @staticmethod
    def create_representative_if_individual(customer):
        if customer.type.name != 'Individual':
            return

        first_name, *last_name_tokens = customer.name.split(' ')
        last_name = last_name_tokens[0] if last_name_tokens else ""

        representative = CustomerRepresentative(
            first_name=first_name,
            last_name=last_name,
            phone_number=customer.phone_number,
            customer=customer,
        )
        representative.save()


class DeleteCustomerView(auth_mixins.PermissionRequiredMixin, views.DeleteView):
    model = Customer
    template_name = 'customer/customer_delete.html'
    success_url = reverse_lazy('customers_list')

    permission_required = ('customers.view_customer', 'customers.change_customer')


class CreateCustomerAssetView(auth_mixins.PermissionRequiredMixin, views.CreateView):
    model = CustomerAsset
    form_class = CreateCustomerAssetForm
    template_name = 'customer_asset/customer_asset_create.html'

    permission_required = 'customers.add_customerasset'

    def get_success_url(self):
        return reverse_lazy('customer_detail', kwargs={'pk': self.object.customer.pk})

    def form_valid(self, form):
        customer_id = self.kwargs['customer_id']
        customer = Customer.objects.get(pk=customer_id)

        customer_asset = form.save(commit=False)
        customer_asset.customer = customer

        customer_asset.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        customer_id = self.kwargs['customer_id']
        if customer_id:
            customer = Customer.objects.prefetch_related('customerasset_set').filter(pk=customer_id).get()
            context['customer'] = customer

        context['asset_categories'] = AssetCategory.objects.all()
        context['brands'] = Brand.objects.all()
        assets = Asset.objects.all()

        # filter assets by brand
        brand = self.request.GET.get('brands', None)
        if brand:
            brand = int(brand)
            if brand > 0:
                assets = assets.filter(brand__pk=brand)

        # filter assets by category
        category = self.request.GET.get('asset_categories', None)
        if category:
            category = int(category)
            if category > 0:
                assets = assets.filter(category__pk=category)

        context['form'].fields['asset'].queryset = assets
        context['asset_cnt'] = len(assets)

        return context


class CustomerAssetDetailView(auth_mixins.PermissionRequiredMixin, views.DetailView):
    model = CustomerAsset
    template_name = 'customer_asset/customer_asset_detail.html'

    permission_required = 'customers.view_customerasset'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        service_orders = ServiceOrderHeader.objects.filter(customer_asset_id=self.object.pk).order_by('-created_on')
        context['service_orders'] = service_orders
        return context


class EditCustomerAssetView(auth_mixins.PermissionRequiredMixin, views.UpdateView):
    model = CustomerAsset
    form_class = EditCustomerAssetForm
    template_name = 'customer_asset/customer_asset_edit.html'

    permission_required = ('customers.view_customerasset', 'customers.change_customerasset')

    def get_success_url(self):
        return reverse_lazy('customer_detail', kwargs={'pk': self.object.customer.pk})


class DeleteCustomerAssetView(auth_mixins.PermissionRequiredMixin, views.DeleteView):
    model = CustomerAsset
    template_name = 'customer_asset/customer_asset_delete.html'

    permission_required = ('customers.view_customerasset', 'customers.change_customerasset')

    def get_success_url(self):
        return reverse_lazy('customer_detail', kwargs={'pk': self.object.customer.pk})


class CreateCustomerRepresentativeView(auth_mixins.PermissionRequiredMixin, views.CreateView):
    model = CustomerRepresentative
    template_name = 'customer_representatives/customer_representatives_create.html'
    form_class = CreateCustomerRepresentativeForm

    permission_required = 'customers.add_customerrepresentative'

    def get_success_url(self):
        return reverse_lazy('customer_detail', kwargs={'pk': self.object.customer.pk}) + '?show_representatives'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        customer_id = self.kwargs['customer_id']
        if customer_id:
            customer = Customer.objects.prefetch_related('customerrepresentative_set').get(pk=customer_id)
            context['customer'] = customer
        return context

    def form_valid(self, form):
        customer_id = self.kwargs['customer_id']
        customer = Customer.objects.get(pk=customer_id)
        customer_representative = form.save(commit=False)

        customer_representative.customer = customer
        customer_representative.save()
        return super().form_valid(form)


class EditCustomerRepresentativeView(auth_mixins.PermissionRequiredMixin, views.UpdateView):
    model = CustomerRepresentative
    template_name = 'customer_representatives/customer_representative_edit.html'
    form_class = EditCustomerRepresentativeForm

    permission_required = ('customers.view_customerrepresentative', 'customers.change_customerrepresentative')

    def get_success_url(self):
        return reverse_lazy('customer_detail', kwargs={'pk': self.object.customer.pk}) + '?show_representatives'


class DeleteCustomerRepresentativeView(auth_mixins.PermissionRequiredMixin, views.DeleteView):
    model = CustomerRepresentative
    template_name = 'customer_representatives/customer_representative_delete.html'

    permission_required = ('customers.view_customerrepresentative', 'customers.change_customerrepresentative')

    def get_success_url(self):
        return reverse_lazy('customer_detail', kwargs={'pk': self.object.customer.pk}) + '?show_representatives'


class CreateCustomerDepartmentView(auth_mixins.PermissionRequiredMixin, views.CreateView):
    model = CustomerDepartment
    template_name = 'customer_department/customer_department_create.html'
    form_class = CreateCustomerDepartmentForm

    permission_required = 'customers.add_customerdepartment'

    def get_success_url(self):
        customer_id = self.kwargs['customer_id']
        if customer_id:
            return reverse_lazy('customer_detail', kwargs={'pk': customer_id}) + '?show_departments'
        return reverse_lazy('customers_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        customer_id = self.kwargs['customer_id']
        if customer_id:
            customer = Customer.objects.prefetch_related('customerdepartment_set').filter(pk=customer_id).get()
            context['customer'] = customer
        return context

    def form_valid(self, form):
        customer_id = self.kwargs['customer_id']
        customer = Customer.objects.get(pk=customer_id)

        customer_department = form.save(commit=False)
        customer_department.customer = customer

        customer_department.save()
        return super().form_valid(form)


class EditCustomerDepartmentView(auth_mixins.PermissionRequiredMixin, views.UpdateView):
    model = CustomerDepartment
    template_name = 'customer_department/customer_department_edit.html'
    form_class = CreateCustomerDepartmentForm

    permission_required = ('customers.view_customerdepartment', 'customers.change_customerdepartment')

    def get_success_url(self):
        customer_id = self.kwargs['customer_id']
        if customer_id:
            return reverse_lazy('customer_detail', kwargs={'pk': customer_id}) + '?show_departments'
        return reverse_lazy('customers_list')


class DeleteCustomerDepartmentView(auth_mixins.PermissionRequiredMixin, views.DeleteView):
    model = CustomerDepartment
    template_name = 'customer_department/customer_department_delete.html'

    permission_required = ('customers.view_customerdepartment', 'customers.change_customerdepartment')

    def get_success_url(self):
        customer_id = self.kwargs['customer_id']
        if customer_id:
            return reverse_lazy('customer_detail', kwargs={'pk': customer_id}) + '?show_departments'
        return reverse_lazy('customers_list')
