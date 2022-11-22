from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from service_manager.customers.models import Customer, CustomerDepartment
from service_manager.master_data.models import CustomerType

UserModel = get_user_model()


class DeleteCustomerDepartmentViewTests(TestCase):
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

        response = self.client.get(reverse('delete_customer_department',
                                           kwargs={'customer_id': customer_department.customer.id,
                                                   'pk': customer_department.pk}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer_department/customer_department_delete.html')

    def test_get__when_user_is_not_logged__expect_to_redirect(self):
        customer_department = CustomerDepartment.objects.first()

        response = self.client.get(reverse('delete_customer_department',
                                           kwargs={'customer_id': customer_department.customer.id,
                                                   'pk': customer_department.pk}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                             f'/accounts/login/?next=/customers/{customer_department.customer.pk}/customer_department/delete/{customer_department.pk}/')

    def test_post__expect_to_delete(self):
        self.client.login(**self.USER_DATA)

        customer_department = CustomerDepartment.objects.first()
        customer = customer_department.customer

        response = self.client.post(reverse('delete_customer_department',
                                            kwargs={'customer_id': customer.id,
                                                    'pk': customer_department.pk}))

        customer_department.refresh_from_db()
        self.assertFalse(customer_department.active)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('customer_detail', kwargs={'pk': customer.pk}))
