from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from service_manager.customers.models import Customer
from service_manager.master_data.models import CustomerType

UserModel = get_user_model()


class CreateCustomerViewTests(TestCase):
    USER_DATA = {
        'email': 'dev@dev.com',
        'password': 'dev',
    }

    def setUp(self):
        UserModel.objects.create_user(**self.USER_DATA)

        CustomerType.objects.create(name='Business')

    def test_get__when_user_is_logged__expect_correct_template(self):
        self.client.login(**self.USER_DATA)

        response = self.client.get(reverse('create_customer'))

        self.assertTemplateUsed(response, 'customer/customer_create.html')
        self.assertEqual(response.status_code, 200)

    def test_get__when_user_is_not_logged__expect_correct_redirect(self):
        response = self.client.get(reverse('create_customer'))

        self.assertRedirects(response, f'/accounts/login/?next=/customers/create/')
        self.assertEqual(response.status_code, 302)

    def test_post__expect_to_create_customer(self):
        self.client.login(**self.USER_DATA)
        customer_type = CustomerType.objects.first()

        data = {
            'name': 'Test Name',
            'vat': 'Test Vat',
            'email_address': 'test@email.com',
            'phone_number': '1233456',
            'type': customer_type.pk,
        }

        response = self.client.post(reverse('create_customer'), data)

        self.assertEqual(response.status_code, 302)
        customer = Customer.objects.first()
        self.assertEqual(data['name'], customer.name)
        self.assertEqual(data['vat'], customer.vat)
        self.assertEqual(data['email_address'], customer.email_address)
        self.assertEqual(data['phone_number'], customer.phone_number)
        self.assertEqual(data['type'], customer.type.pk)
        self.assertRedirects(response, '/customers/')

    def test_post__when_data_invalid__except_not_to_save(self):
        self.client.login(**self.USER_DATA)
        customer_type = CustomerType.objects.first()

        data = {
            'name': 'Test Name',
            'vat': 'Test Vat',
            'email_address': 'test',
            'phone_number': '1233456',
            'type': customer_type.pk,
        }

        response = self.client.post(reverse('create_customer'), data)
        self.assertFalse(response.context_data['form'].is_valid())
        self.assertEqual(response.status_code, 200)
        customers = Customer.objects.count()
        self.assertEqual(customers, 0)