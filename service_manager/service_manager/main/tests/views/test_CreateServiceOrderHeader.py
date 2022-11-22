from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from service_manager.customers.models import CustomerAsset, Customer, CustomerDepartment, CustomerRepresentative
from service_manager.main.models import ServiceOrderHeader
from service_manager.master_data.models import Asset, Brand, AssetCategory, CustomerType

UserModel = get_user_model()


class CreateServiceOrderHeaderTests(TestCase):
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
            name='Mobile',
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

        CustomerAsset.objects.create(
            customer=customer,
            asset=asset,
            serial_number='SN-Apple-21',
            product_number='California-PN_33',
        )

    def test_get__when_user_is_logged__expect_correct_template(self):
        self.client.login(**self.USER_DATA)

        customer_asset = CustomerAsset.objects.first()

        response = self.client.get(reverse('create_service_order', kwargs={'customer_id': customer_asset.customer.id,
                                                                           'asset_id': customer_asset.pk}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'service_order_header/core/service_order_create.html')

    def test_get__when_user_is_not_logged__expect_to_redirect(self):
        customer_asset = CustomerAsset.objects.first()

        response = self.client.get(reverse('create_service_order', kwargs={'customer_id': customer_asset.customer.id,
                                                                           'asset_id': customer_asset.pk}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                             f'/accounts/login/?next=/service_order/customer/{customer_asset.customer.id}/asset/{customer_asset.pk}/create/')

    def test_get__expect_correct_context(self):
        self.client.login(**self.USER_DATA)

        customer_asset = CustomerAsset.objects.first()

        response = self.client.get(reverse('create_service_order', kwargs={'customer_id': customer_asset.customer.id,
                                                                           'asset_id': customer_asset.pk}))

        self.assertEqual(customer_asset, response.context['customer_asset'])
        self.assertEqual(customer_asset.customer, response.context['customer'])

    def test_get__expect_form_to_populate_correctly(self):
        self.client.login(**self.USER_DATA)

        customer_asset = CustomerAsset.objects.first()

        response = self.client.get(reverse('create_service_order', kwargs={'customer_id': customer_asset.customer.id,
                                                                           'asset_id': customer_asset.pk}))

        self.assertEqual(response.context['form'].initial['customer'], customer_asset.customer.id)

    def test_post__when_data_is_valid__expect_to_save(self):
        self.client.login(**self.USER_DATA)

        customer_asset = CustomerAsset.objects.first()

        department = CustomerDepartment.objects.create(
            customer=customer_asset.customer,
            name='HR',
        )

        customer_representative = CustomerRepresentative.objects.create(
            customer=customer_asset.customer,
            first_name='John',
            last_name='Doe',
            email_address='john@doe.com',
            phone_number='1234567890',
        )

        data = {
            'department': department.pk,
            'handed_over_by': customer_representative.pk,
            'problem_description': 'There is a problem...',
        }

        response = self.client.post(reverse('create_service_order', kwargs={'customer_id': customer_asset.customer.id,
                                                                            'asset_id': customer_asset.pk}), data)

        service_order = ServiceOrderHeader.objects.first()
        user = UserModel.objects.first()
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('detail_service_order', kwargs={'pk': service_order.pk}))
        self.assertEqual(service_order.problem_description, data['problem_description'])
        self.assertEqual(service_order.handed_over_by, customer_representative)
        self.assertEqual(service_order.department, department)
        self.assertEqual(service_order.accepted_by, user)
        self.assertEqual(service_order.customer, customer_asset.customer)
        self.assertEqual(service_order.customer_asset, customer_asset)

    def test_post__when_data_is_invalid__expect_not_to_save(self):
        self.client.login(**self.USER_DATA)

        customer_asset = CustomerAsset.objects.first()

        department = CustomerDepartment.objects.create(
            customer=customer_asset.customer,
            name='HR',
        )

        customer_representative = CustomerRepresentative.objects.create(
            customer=customer_asset.customer,
            first_name='John',
            last_name='Doe',
            email_address='john@doe.com',
            phone_number='1234567890',
        )

        data = {
            'department': department.pk,
            'handed_over_by': customer_representative.pk,
            'problem_description': '',
        }

        response = self.client.post(reverse('create_service_order', kwargs={'customer_id': customer_asset.customer.id,
                                                                            'asset_id': customer_asset.pk}), data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(ServiceOrderHeader.objects.count(), 0)
        self.assertFalse(response.context_data['form'].is_valid())
