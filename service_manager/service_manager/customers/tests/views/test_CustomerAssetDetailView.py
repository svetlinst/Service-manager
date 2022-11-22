from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from service_manager.customers.models import Customer, CustomerAsset
from service_manager.main.models import ServiceOrderHeader
from service_manager.master_data.models import CustomerType, AssetCategory, Brand, Asset

UserModel = get_user_model()


class CustomerAssetDetailViewTests(TestCase):
    USER_DATA = {
        'email': 'dev@dev.com',
        'password': 'dev',
    }

    def setUp(self):
        UserModel.objects.create_user(**self.USER_DATA)

        customer_type = CustomerType.objects.create(name='Business')
        customer = Customer.objects.create(
            name='Test Customer Name',
            vat='123456789',
            email_address='test@test.com',
            phone_number='987654321',
            type=customer_type,
        )

        category = AssetCategory.objects.create(
            name='PC',
        )

        brand = Brand.objects.create(
            name='HP',
        )

        asset = Asset.objects.create(
            category=category,
            brand=brand,
            model_name='Envy 01',
            model_number='007',
        )

        customer_asset1 = CustomerAsset.objects.create(
            customer=customer,
            asset=asset,
            serial_number='SN12345',
            product_number='PN98765',
        )

        CustomerAsset.objects.create(
            customer=customer,
            asset=asset,
            serial_number='TESTSN',
            product_number='PNTEST',
        )

        ServiceOrderHeader.objects.create(
            customer=customer,
            customer_asset=customer_asset1,
            problem_description='Some description test',
        )

    def test_get__when_user_is_logged__expect_correct_template(self):
        self.client.login(**self.USER_DATA)

        customer = Customer.objects.first()
        customer_asset = CustomerAsset.objects.first()
        response = self.client.get(
            reverse('customer_asset_detail', kwargs={'customer_id': customer.pk, 'pk': customer_asset.pk}))

        self.assertTemplateUsed(response, 'customer_asset/customer_asset_detail.html')

    def test_get__when_user_is_not_logged__expect_to_redirect(self):
        customer = Customer.objects.first()
        customer_asset = CustomerAsset.objects.first()
        response = self.client.get(
            reverse('customer_asset_detail', kwargs={'customer_id': customer.pk, 'pk': customer_asset.pk}))

        self.assertRedirects(response,
                             f'/accounts/login/?next=/customers/{customer.pk}/customer_asset/detail/{customer_asset.pk}/')
        self.assertEqual(response.status_code, 302)

    def test_get__expect_correct_context(self):
        self.client.login(**self.USER_DATA)

        customer = Customer.objects.first()
        customer_asset = CustomerAsset.objects.first()
        response = self.client.get(
            reverse('customer_asset_detail', kwargs={'customer_id': customer.pk, 'pk': customer_asset.pk}))

        self.assertIn('service_orders', response.context)

    def test_get__when_there_is_service_order__expect_correct_context(self):
        self.client.login(**self.USER_DATA)

        customer = Customer.objects.first()
        service_order_header = ServiceOrderHeader.objects.first()
        customer_asset = service_order_header.customer_asset

        response = self.client.get(
            reverse('customer_asset_detail', kwargs={'customer_id': customer.pk, 'pk': customer_asset.pk}))

        self.assertIn('service_orders', response.context)

        service_order = response.context['service_orders'][0]
        self.assertEqual(service_order, service_order_header)
