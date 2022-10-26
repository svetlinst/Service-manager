from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from service_manager.customers.models import Customer
from service_manager.master_data.models import CustomerType

UserModel = get_user_model()


class CustomersListViewTests(TestCase):
    def test_get__when_user_is_logged__expect_correct_template(self):
        user_data = {
            'email': 'dev@dev.com',
            'password': 'dev',
        }

        UserModel.objects.create_user(**user_data)

        self.client.login(**user_data)

        response = self.client.get(reverse('customers_list'))

        self.assertTemplateUsed(response, 'customer/customers.html')

    def test_get__when_user_is_not_logged_expect_redirect(self):
        response = self.client.get(reverse('customers_list'))

        self.assertRedirects(response, '/accounts/login/?next=/customers/')

    def test_get__when_searching_for_customers__expect_correct(self):
        user_data = {
            'email': 'dev@dev.com',
            'password': 'dev',
        }
        UserModel.objects.create_user(**user_data)
        self.client.login(**user_data)

        data = {
            'search_value': 'test',
        }

        customer_type = CustomerType.objects.create(name='Business')

        customers_to_create = (
            Customer(name='Customer Nametest', vat='123456789', email_address='test@test.com', phone_number='123456789',
                     type=customer_type),
            Customer(name='Customer Name', vat='123456789', email_address='test2@test.com', phone_number='123456789',
                     type=customer_type),
        )

        Customer.objects.bulk_create(customers_to_create)

        response = self.client.get(reverse('customers_list'), data=data)

        customers = response.context['object_list']
        self.assertEqual(len(customers), 1)

    def test_get__when_not_performing_search_expect_correct(self):
        user_data = {
            'email': 'dev@dev.com',
            'password': 'dev',
        }
        UserModel.objects.create_user(**user_data)
        self.client.login(**user_data)

        customer_type = CustomerType.objects.create(name='Other')

        customers_to_create = (
            Customer(name='Customer Nametest', vat='123456789', email_address='test@test.com', phone_number='123456789',
                     type=customer_type),
            Customer(name='Customer Name', vat='123456789', email_address='test2@test.com', phone_number='123456789',
                     type=customer_type),
        )

        Customer.objects.bulk_create(customers_to_create)

        response = self.client.get(reverse('customers_list'))

        customers = response.context['object_list']
        self.assertEqual(len(customers), 2)
