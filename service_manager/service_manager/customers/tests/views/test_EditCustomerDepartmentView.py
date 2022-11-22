from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
import random

from service_manager.customers.models import Customer, CustomerDepartment
from service_manager.master_data.models import CustomerType

UserModel = get_user_model()


class EditCustomerDepartmentViewTests(TestCase):
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

        customer_department = CustomerDepartment.objects.first()

        response = self.client.get(reverse('edit_customer_department',
                                           kwargs={'customer_id': customer_department.customer.id,
                                                   'pk': customer_department.pk}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer_department/customer_department_edit.html')

    def test_get__when_user_is_not_logged__expect_to_redirect(self):
        customer_department = CustomerDepartment.objects.first()

        response = self.client.get(reverse('edit_customer_department',
                                           kwargs={'customer_id': customer_department.customer.id,
                                                   'pk': customer_department.pk}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                             f'/accounts/login/?next=/customers/{customer_department.customer.pk}/customer_department/edit/{customer_department.pk}/')

    def test_post__when_data_is_valid__expect_to_update(self):
        self.client.login(**self.USER_DATA)

        customer_department = CustomerDepartment.objects.first()

        data = {
            'name': 'DevOps',
        }

        response = self.client.post(reverse('edit_customer_department',
                                            kwargs={'customer_id': customer_department.customer.id,
                                                    'pk': customer_department.pk}), data)

        customer_department.refresh_from_db()
        self.assertEqual(customer_department.name, data['name'])
        self.assertRedirects(response,
                             reverse('customer_detail', kwargs={'pk': customer_department.customer.pk}))

    def test_post__when_data_is_invalid__expect_not_to_update(self):
        self.client.login(**self.USER_DATA)

        customer_department = CustomerDepartment.objects.first()

        data = {
            'name': ''.join(random.choice('abcdefgh') for x in range(101)),
        }

        response = self.client.post(reverse('edit_customer_department',
                                            kwargs={'customer_id': customer_department.customer.id,
                                                    'pk': customer_department.pk}), data)

        customer_department.refresh_from_db()
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(customer_department.name, data['name'])
        self.assertFalse(response.context['form'].is_valid())
