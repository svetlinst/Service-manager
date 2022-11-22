from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from service_manager.customers.models import Customer
from service_manager.master_data.models import CustomerType

UserModel = get_user_model()


class EditCustomerViewTests(TestCase):
    USER_DATA = {
        'email': 'dev@dev.com',
        'password': 'dev',
    }

    def setUp(self):
        UserModel.objects.create_user(**self.USER_DATA)

        customer_type = CustomerType.objects.create(name='Business')
        Customer.objects.create(
            name='Test Customer Name',
            vat='123456789',
            email_address='test@test.com',
            phone_number='987654321',
            type=customer_type,
        )

    def test_get__when_user_logged__expect_correct_template(self):
        self.client.login(**self.USER_DATA)
        customer = Customer.objects.first()
        response = self.client.get(reverse('edit_customer', kwargs={'pk': customer.pk}))

        self.assertTemplateUsed(response, 'customer/customer_edit.html')

    def test_get__when_user_not_logged__expect_redirect(self):
        customer = Customer.objects.first()
        response = self.client.get(reverse('edit_customer', kwargs={'pk': customer.pk}))

        self.assertRedirects(response, f'/accounts/login/?next=/customers/{customer.pk}/')

    def test_post__when_valid_data__expect_correct_redirect(self):
        self.client.login(**self.USER_DATA)
        customer = Customer.objects.first()
        data = {
            'name': 'Updated Name',
            'vat': customer.vat,
            'email_address': customer.email_address,
            'phone_number': customer.phone_number,
            'type': customer.type.id,
        }
        response = self.client.post(reverse('edit_customer', kwargs={'pk': customer.pk}), data)

        customer.refresh_from_db()
        self.assertEqual(customer.name, 'Updated Name')

        self.assertEqual(response.status_code, 302)

        self.assertRedirects(response, f'/customers/detail/{customer.pk}/')

