from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from service_manager.customers.models import Customer, CustomerAsset
from service_manager.master_data.models import CustomerType, AssetCategory, Brand, Asset

UserModel = get_user_model()


class CreateCustomerAssetViewTests(TestCase):
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

        Asset.objects.create(
            category=category,
            brand=brand,
            model_name='Envy 01',
            model_number='007',
        )

    def test_get__when_user_is_logged__expect_correct_template(self):
        self.client.login(**self.USER_DATA)
        customer = Customer.objects.first()

        response = self.client.get(reverse('create_customer_asset', kwargs={'customer_id': customer.pk}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer_asset/customer_asset_create.html')

    def test_get__when_user_is_not_logged__expect_to_redirect(self):
        customer = Customer.objects.first()

        response = self.client.get(reverse('create_customer_asset', kwargs={'customer_id': customer.pk}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/accounts/login/?next=/customers/{customer.pk}/customer_asset/create/')

    def test_post__expect_to_create_customer_asset(self):
        self.client.login(**self.USER_DATA)
        customer = Customer.objects.first()
        asset = Asset.objects.first()

        data = {
            'customer': customer.pk,
            'asset': asset.pk,
            'serial_number': 'sn1234',
            'product_number': 'pn1234',
        }

        response = self.client.post(reverse('create_customer_asset', kwargs={'customer_id': customer.pk}), data)

        self.assertEqual(response.status_code, 302)
        customer_asset = CustomerAsset.objects.first()
        self.assertIsNotNone(customer_asset)
        self.assertRedirects(response, reverse('customer_detail', kwargs={'pk': customer.pk}))
        self.assertEqual(data['customer'], customer_asset.customer.pk)
        self.assertEqual(data['asset'], customer_asset.asset.pk)
        self.assertEqual(data['serial_number'], customer_asset.serial_number)
        self.assertEqual(data['product_number'], customer_asset.product_number)

    def test_post__when_data_is_invalid__expect_not_to_save(self):
        self.client.login(**self.USER_DATA)
        customer = Customer.objects.first()
        asset = Asset.objects.first()

        data = {
            'customer': customer.pk,
            'asset': asset.pk,
            'serial_number': '12345678901234567890123',
            'product_number': 'pn1234',
        }

        response = self.client.post(reverse('create_customer_asset', kwargs={'customer_id': customer.pk}), data)
        self.assertEqual(response.status_code, 200)

        customer_asset = CustomerAsset.objects.first()
        self.assertIsNone(customer_asset)

        self.assertFalse(response.context_data['form'].is_valid())

    def test_get__expect_correct_context_data(self):
        self.client.login(**self.USER_DATA)
        customer = Customer.objects.first()

        response = self.client.get(reverse('create_customer_asset', kwargs={'customer_id': customer.pk}))

        self.assertEqual(customer, response.context['customer'])
        self.assertIn('customer', response.context)