from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from service_manager.customers.models import Customer, CustomerAsset
from service_manager.master_data.models import CustomerType, AssetCategory, Brand, Asset

UserModel = get_user_model()


class EditCustomerAssetView(TestCase):
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

        CustomerAsset.objects.create(
            customer=customer,
            asset=asset,
            serial_number='TESTSN',
            product_number='PNTEST',
        )

    def test_get__when_user_is_logged_expect_correct_template(self):
        self.client.login(**self.USER_DATA)
        customer = Customer.objects.first()
        customer_asset = CustomerAsset.objects.first()

        response = self.client.get(
            reverse('edit_customer_asset', kwargs={'customer_id': customer.pk, 'pk': customer_asset.pk}))

        self.assertTemplateUsed(response, 'customer_asset/customer_asset_edit.html')
        self.assertEqual(response.status_code, 200)

    def test_get__when_user_is_not_logged__expect_to_redirect(self):
        customer = Customer.objects.first()
        customer_asset = CustomerAsset.objects.first()

        response = self.client.get(
            reverse('edit_customer_asset', kwargs={'customer_id': customer.pk, 'pk': customer_asset.pk}))

        self.assertRedirects(response,
                             f'/accounts/login/?next=/customers/{customer.pk}/customer_asset/{customer_asset.pk}/')
        self.assertEqual(response.status_code, 302)

    def test_post__when_data_is_correct__expect_to_update(self):
        self.client.login(**self.USER_DATA)
        customer = Customer.objects.first()
        customer_asset = CustomerAsset.objects.first()

        data = {
            'customer': customer.pk,
            'asset': customer_asset.pk,
            'serial_number': 'updatedSN',
            'product_number': 'updatedPN',
        }

        response = self.client.post(
            reverse('edit_customer_asset', kwargs={'customer_id': customer.pk, 'pk': customer_asset.pk}), data)

        customer_asset.refresh_from_db()
        self.assertEqual(data['serial_number'], customer_asset.serial_number)
        self.assertEqual(data['product_number'], customer_asset.product_number)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('customer_detail', kwargs={'pk': customer.pk}))

    def test_post__when_data_is_invalid__expect_not_to_update(self):
        self.client.login(**self.USER_DATA)

        customer = Customer.objects.first()
        customer_asset = CustomerAsset.objects.first()

        data = {
            'customer': customer.pk,
            'asset': customer_asset.pk,
            'serial_number': '12345678901234567890123',
            'product_number': 'updatedPN',
        }

        response = self.client.post(
            reverse('edit_customer_asset', kwargs={'customer_id': customer.pk, 'pk': customer_asset.pk}), data)

        customer_asset.refresh_from_db()
        self.assertNotEqual(data['serial_number'], customer_asset.serial_number)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context_data['form'].is_valid())
