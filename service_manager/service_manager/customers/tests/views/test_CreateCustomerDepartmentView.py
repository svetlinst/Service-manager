from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
import random

from service_manager.customers.models import Customer, CustomerDepartment
from service_manager.master_data.models import CustomerType

UserModel = get_user_model()


class CreateCustomerDepartmentTests(TestCase):
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

        CustomerDepartment.objects.create(
            customer=customer,
            name='Accounting',
        )

    def test_get__when_user_is_logged__expect_correct_template(self):
        self.client.login(**self.USER_DATA)

        customer = Customer.objects.first()

        response = self.client.get(reverse('create_customer_department', kwargs={'customer_id': customer.pk}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer_department/customer_department_create.html')
        self.assertIn('customer', response.context)
        self.assertEqual(customer, response.context['customer'])

    def test_get__when_user_is_not_logged__expect_to_redirect(self):
        customer = Customer.objects.first()

        response = self.client.get(reverse('create_customer_department', kwargs={'customer_id': customer.pk}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/accounts/login/?next=/customers/{customer.pk}/customer_department/create/')

    def test_post__when_data_is_valid__expect_to_create(self):
        self.client.login(**self.USER_DATA)

        customer = Customer.objects.first()

        data = {
            'name': 'Human Resources',
        }

        response = self.client.post(reverse('create_customer_department', kwargs={'customer_id': customer.pk}), data)

        customer_departments = CustomerDepartment.objects.all()
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('customer_detail', kwargs={'pk': customer.pk}))
        self.assertEqual(len(customer_departments), 2)
        self.assertEqual(customer_departments[1].name, data['name'])

    def test_post__when_data_is_invalid__expect_not_to_save(self):
        self.client.login(**self.USER_DATA)

        customer = Customer.objects.first()

        data = {
            'name': ''.join(random.choice('abcdefgh') for x in range(101)),
        }

        response = self.client.post(reverse('create_customer_department', kwargs={'customer_id': customer.pk}), data)

        customer_departments = CustomerDepartment.objects.all()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(customer_departments), 1)
        self.assertFalse(response.context_data['form'].is_valid())
