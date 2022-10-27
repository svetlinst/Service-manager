from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from service_manager.customers.models import Customer, CustomerRepresentative
from service_manager.master_data.models import CustomerType

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

    def test_get__when_user_is_logged__expect_correct_template(self):
        self.client.login(**self.USER_DATA)

        response = self.client.get(reverse('customer_detail', kwargs={'pk': 1}))

        self.assertTemplateUsed(response, 'customer/customer_detail.html')

    def test_get__when_user_is_not_logged_expect_redirect(self):
        response = self.client.get(reverse('customer_detail', kwargs={'pk': 1}))

        self.assertRedirects(response, '/accounts/login/?next=/customers/detail/1/')

    def test_get__when_filter_is_not_used__expect_two_representatives(self):
        self.client.login(**self.USER_DATA)
        response = self.client.get(reverse('customer_detail', kwargs={'pk': 1}))

        representatives = response.context['customer_representatives']

        self.assertEqual(len(representatives), 2)

    def test_get__when_filter_is_not_used__expect_zero_representatives(self):
        self.client.login(**self.USER_DATA)
        response = self.client.get(reverse('customer_detail', kwargs={'pk': 2}))

        representatives = response.context['customer_representatives']

        self.assertEqual(len(representatives), 0)
