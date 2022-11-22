from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from service_manager.customers.models import Customer, CustomerAsset
from service_manager.main.models import ServiceOrderHeader
from service_manager.master_data.models import CustomerType, AssetCategory, Brand, Asset

UserModel = get_user_model()


class ServiceOrderHeaderDetailViewTests(TestCase):
    USER_DATA = {
        'email': 'dev@dev.com',
        'password': 'dev',
    }

    def setUp(self):
        UserModel.objects.create_user(**self.USER_DATA)

        customer_type = CustomerType.objects.create(
            name='Business'
        )

        customer = Customer.objects.create(
            type=customer_type,
            name='Testing Inc.',
            vat='123444121',
            email_address='testing@inc.com',
            phone_number='100921122',
        )

        category = AssetCategory.objects.create(
            name='Monilr',
        )

        brand = Brand.objects.create(
            name='Apple',
        )

        asset = Asset.objects.create(
            category=category,
            brand=brand,
            model_name='iPhone',
            model_number='13 Pro',
        )

        customer_asset1 = CustomerAsset.objects.create(
            customer=customer,
            asset=asset,
            serial_number='SN-Apple-21',
            product_number='California-PN_33',
        )

        ServiceOrderHeader.objects.create(
            customer=customer,
            customer_asset=customer_asset1,
            problem_description='First SOH Description',
        )

    def test_get__when_user_is_logged__expect_correct_template(self):
        self.client.login(**self.USER_DATA)

        service_order = ServiceOrderHeader.objects.first()

        response = self.client.get(reverse('detail_service_order', kwargs={'pk': service_order.pk}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'service_order_header/core/service_order_details.html')

    def test_get__when_use_is_not_logged__expect_to_redirect(self):
        service_order = ServiceOrderHeader.objects.first()

        response = self.client.get(reverse('detail_service_order', kwargs={'pk': service_order.pk}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/accounts/login/?next=/service_order/{service_order.pk}/')
