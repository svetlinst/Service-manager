from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from service_manager.customers.models import Customer
from service_manager.master_data.models import CustomerType

UserModel = get_user_model()


class DeleteCustomerViewTests(TestCase):
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

    def test_get__when_the_user_is_logged__expect_correct_template(self):
        self.client.login(**self.USER_DATA)
        customer = Customer.objects.first()

        response = self.client.get(reverse('delete_customer', kwargs={'pk': customer.pk}))

        self.assertTemplateUsed(response, 'customer/customer_delete.html')
        self.assertEqual(response.status_code, 200)

    def test_get__when_the_user_is_not_logged__expect_to_redirect_to_login(self):
        customer = Customer.objects.first()
        response = self.client.get(reverse('delete_customer', kwargs={'pk': customer.pk}))

        self.assertRedirects(response, f'/accounts/login/?next=/customers/delete/{customer.pk}')
        self.assertEqual(response.status_code, 302)