from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from service_manager.customers.models import Customer, CustomerAsset
from service_manager.main.models import ServiceOrderHeader
from service_manager.master_data.models import CustomerType, AssetCategory, Brand, Asset

UserModel = get_user_model()


class ServiceOrderHeaderPendingServiceListViewTests(TestCase):
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

        asset2 = Asset.objects.create(
            category=category,
            brand=brand,
            model_name='MacBook',
            model_number='14 Inch Pro',
        )

        customer_asset1 = CustomerAsset.objects.create(
            customer=customer,
            asset=asset,
            serial_number='SN-Apple-21',
            product_number='California-PN_33',
        )

        customer_asset2 = CustomerAsset.objects.create(
            customer=customer,
            asset=asset2,
            serial_number='MB-14-22',
            product_number='MBook PR-44',
        )

        ServiceOrderHeader.objects.create(
            customer=customer,
            customer_asset=customer_asset1,
            problem_description='First SOH Description',
        )

        ServiceOrderHeader.objects.create(
            customer=customer,
            customer_asset=customer_asset2,
            problem_description='Second SOH Description',
        )

    def test_get__when_user_is_logged__expect_correct_template(self):
        self.client.login(**self.USER_DATA)

        response = self.client.get(reverse('service_orders_list_pending_service'))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'service_order_header/list_views/service_orders_service.html')

    def test_get__when_user_is_not_logged__expect_to_redirect(self):
        response = self.client.get(reverse('service_orders_list_pending_service'))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/service_orders/pending/')

    def test_get__when_all_are_pending_expect_correct_queryset(self):
        self.client.login(**self.USER_DATA)

        response = self.client.get(reverse('service_orders_list_pending_service'))

        service_orders = ServiceOrderHeader.objects.filter(is_serviced=False)
        context = response.context['object_list']
        self.assertEqual(len(context), len(service_orders))
        self.assertQuerysetEqual(context, service_orders, transform=lambda x: x)

    def test_get__when_one_is_serviced_expect_correct_queryset(self):
        self.client.login(**self.USER_DATA)

        first_service_order = ServiceOrderHeader.objects.first()
        first_service_order.is_serviced = True
        first_service_order.save()

        response = self.client.get(reverse('service_orders_list_pending_service'))

        service_orders = ServiceOrderHeader.objects.filter(is_serviced=False)
        context = response.context['object_list']
        self.assertEqual(len(context), 1)
        self.assertQuerysetEqual(context, service_orders, transform=lambda x: x)
