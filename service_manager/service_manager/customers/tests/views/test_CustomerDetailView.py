from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from service_manager.customers.models import Customer, CustomerRepresentative, CustomerAsset, CustomerDepartment
from service_manager.main.models import ServiceOrderHeader
from service_manager.master_data.models import CustomerType, AssetCategory, Brand, Asset

UserModel = get_user_model()


class CustomerDetailViewTests(TestCase):
    USER_DATA = {
        'email': 'dev@dev.com',
        'password': 'dev',
    }

    def setUp(self):
        UserModel.objects.create_user(**self.USER_DATA)

        customer_type = CustomerType.objects.create(name='Business')
        first_customer = Customer.objects.create(
            name='Test Customer Name',
            vat='123456789',
            email_address='test@test.com',
            phone_number='987654321',
            type=customer_type,
        )

        second_customer = Customer.objects.create(
            name='Another Customer Name',
            vat='1122334455',
            email_address='another@another.com',
            phone_number='9988776655',
            type=customer_type,
        )

        CustomerRepresentative.objects.create(
            first_name='First',
            last_name='Last',
            email_address='f_name@lname.com',
            phone_number='1133557799',
            customer=first_customer,
        )

        CustomerRepresentative.objects.create(
            first_name='John',
            last_name='Doe',
            email_address='doe@john.com',
            phone_number='1234556',
            customer=first_customer,
        )

        category = AssetCategory.objects.create(
            name='PC',
        )

        brand = Brand.objects.create(
            name='HP',
        )

        first_asset = Asset.objects.create(
            category=category,
            brand=brand,
            model_name='Envy 01',
            model_number='007',
        )

        second_asset = Asset.objects.create(
            category=category,
            brand=brand,
            model_name='Z-Book',
            model_number='1020',
        )

        CustomerAsset.objects.create(
            asset=first_asset,
            customer=first_customer,
            serial_number='SN001',
            product_number='PN001',
        )

        CustomerAsset.objects.create(
            asset=second_asset,
            customer=first_customer,
            serial_number='SNtest001',
            product_number='PNtest001',
        )

        CustomerDepartment.objects.create(
            customer=first_customer,
            name='Accounting',
        )

        CustomerDepartment.objects.create(
            customer=first_customer,
            name='Human Resources',
        )

    def test_get__when_user_is_logged__expect_correct_template(self):
        self.client.login(**self.USER_DATA)
        customer = Customer.objects.first()
        response = self.client.get(reverse('customer_detail', kwargs={'pk': customer.pk}))

        self.assertTemplateUsed(response, 'customer/customer_detail.html')

    def test_get__when_user_is_not_logged_expect_redirect(self):
        customer = Customer.objects.first()
        response = self.client.get(reverse('customer_detail', kwargs={'pk': customer.pk}))

        self.assertRedirects(response, f'/accounts/login/?next=/customers/detail/{customer.pk}/')

    def test_get__when_filter_is_not_used__expect_two_representatives(self):
        self.client.login(**self.USER_DATA)
        customer = Customer.objects.first()

        response = self.client.get(reverse('customer_detail', kwargs={'pk': customer.pk}))

        representatives = response.context['customer_representatives']

        self.assertEqual(len(representatives), 2)

    def test_get__when_filter_is_not_used__expect_zero_representatives(self):
        self.client.login(**self.USER_DATA)
        customer = Customer.objects.all()[1]

        response = self.client.get(reverse('customer_detail', kwargs={'pk': customer.pk}))

        representatives = response.context['customer_representatives']

        self.assertEqual(len(representatives), 0)

    def test_get__when_filter_is_used__expect_one_representative(self):
        self.client.login(**self.USER_DATA)
        customer = Customer.objects.first()

        data = {
            'representative': 'ohn',
        }

        response = self.client.get(reverse('customer_detail', kwargs={'pk': customer.pk}), data=data)

        representatives = response.context['customer_representatives']

        self.assertEqual(len(representatives), 1)

    def test_get__when_filter_is_used__expect_zero_representative(self):
        self.client.login(**self.USER_DATA)
        customer = Customer.objects.first()
        data = {
            'representative': 'zzz',
        }

        response = self.client.get(reverse('customer_detail', kwargs={'pk': customer.pk}), data=data)

        representatives = response.context['customer_representatives']

        self.assertEqual(len(representatives), 0)

    def test_get__when_filter_is_not_used__expect_two_assets(self):
        self.client.login(**self.USER_DATA)
        customer = Customer.objects.first()
        response = self.client.get(reverse('customer_detail', kwargs={'pk': customer.pk}))

        customer_assets = response.context['customer_assets']

        self.assertEqual(len(customer_assets), 2)

    def test_get__when_customer_has_no_assets__expect_zero_assets(self):
        self.client.login(**self.USER_DATA)
        customer = Customer.objects.all()[1]
        response = self.client.get(reverse('customer_detail', kwargs={'pk': customer.pk}))

        customer_assets = response.context['customer_assets']

        self.assertEqual(len(customer_assets), 0)

    def test_get__when_customer_has_two_assets_with_filter__expect_one_asset(self):
        self.client.login(**self.USER_DATA)
        customer = Customer.objects.first()

        data = {
            'search_value': 'sntest',
        }

        response = self.client.get(reverse('customer_detail', kwargs={'pk': customer.pk}), data=data)

        customer_assets = response.context['customer_assets']

        self.assertEqual(len(customer_assets), 1)

    def test_get__when_customer_has_assets_do_not_meet_search_criteria__expect_zero_assets(self):
        self.client.login(**self.USER_DATA)
        customer = Customer.objects.first()
        data = {
            'search_value': 'z',
        }

        response = self.client.get(reverse('customer_detail', kwargs={'pk': customer.pk}), data=data)

        customer_assets = response.context['customer_assets']

        self.assertEqual(len(customer_assets), 0)

    def test_get__when_asset_is_being_serviced__expect_correct_status(self):
        self.client.login(**self.USER_DATA)
        customer = Customer.objects.prefetch_related('customerasset_set').first()
        customer_assets = CustomerAsset.objects.filter(customer=customer)

        ServiceOrderHeader.objects.create(
            customer=customer,
            customer_asset=customer_assets.first(),
            problem_description='Some description',
        )

        response = self.client.get(reverse('customer_detail', kwargs={'pk': customer.pk}))

        assets_being_serviced = response.context['assets_being_serviced']

        self.assertEqual(len(assets_being_serviced), 1)

    def test_get__when_filter_is_not_used__expect_two_departments(self):
        self.client.login(**self.USER_DATA)
        customer = Customer.objects.first()
        response = self.client.get(reverse('customer_detail', kwargs={'pk': customer.pk}))

        customer_departments = response.context['customer_departments']

        self.assertEqual(len(customer_departments), 2)

    def test_get__when_customer_has_no_departments__expect_zero_departments(self):
        self.client.login(**self.USER_DATA)
        customer = Customer.objects.all()[1]
        response = self.client.get(reverse('customer_detail', kwargs={'pk': customer.pk}))

        customer_departments = response.context['customer_departments']

        self.assertEqual(len(customer_departments), 0)

    def test_get__when_customer_has_two_departments_with_filter__expect_one_department(self):
        self.client.login(**self.USER_DATA)
        customer = Customer.objects.first()

        data = {
            'departments': ' ',
        }

        response = self.client.get(reverse('customer_detail', kwargs={'pk': customer.pk}), data=data)

        customer_departments = response.context['customer_departments']

        self.assertEqual(len(customer_departments), 1)

    def test_get__when_customer_has_departments_do_not_meet_search_criteria__expect_zero_departments(self):
        self.client.login(**self.USER_DATA)
        customer = Customer.objects.first()
        data = {
            'departments': 'z',
        }

        response = self.client.get(reverse('customer_detail', kwargs={'pk': customer.pk}), data=data)

        customer_departments = response.context['customer_departments']

        self.assertEqual(len(customer_departments), 0)
