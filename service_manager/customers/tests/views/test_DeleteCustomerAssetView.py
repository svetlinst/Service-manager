from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from service_manager.customers.models import Customer, CustomerAsset
from service_manager.master_data.models import CustomerType, AssetCategory, Brand, Asset

UserModel = get_user_model()


class DeleteCustomerAssetViewTests(TestCase):
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

    def test_get__when_user_is_logged__expect_correct_template(self):
        self.client.login(**self.USER_DATA)

        customer_asset = CustomerAsset.objects.first()

        response = self.client.get(reverse('delete_customer_asset',
                                           kwargs={'customer_id': customer_asset.customer.id, 'pk': customer_asset.pk}))

        self.assertTemplateUsed(response, 'customer_asset/customer_asset_delete.html')
        self.assertEqual(response.status_code, 200)

    def test_get__when_user_is_not_logged__expect_to_redirect(self):
        customer_asset = CustomerAsset.objects.first()

        response = self.client.get(reverse('delete_customer_asset',
                                           kwargs={'customer_id': customer_asset.customer.id, 'pk': customer_asset.pk}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                             f'/accounts/login/?next=/customers/{customer_asset.customer.pk}/customer_asset/delete/{customer_asset.pk}/')

    def test_post__expect_to_delete_asset(self):
        self.client.login(**self.USER_DATA)
        customer_asset = CustomerAsset.objects.first()
        self.assertTrue(customer_asset.active)

        response = self.client.post(reverse('delete_customer_asset',
                                            kwargs={'customer_id': customer_asset.customer.id,
                                                    'pk': customer_asset.pk}))

        customer_asset.refresh_from_db()
        self.assertFalse(customer_asset.active)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('customer_detail', kwargs={'pk': customer_asset.customer.pk}))
