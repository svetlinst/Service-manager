from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from service_manager.customers.models import Customer, CustomerRepresentative
from service_manager.master_data.models import CustomerType

UserModel = get_user_model()


class EditCustomerRepresentativeViewTests(TestCase):
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

        CustomerRepresentative.objects.create(
            customer=customer,
            first_name='John',
            last_name='Doe',
            email_address='john@doe.com',
            phone_number='123456789001',
        )

    def test_get__when_user_is_logged__expect_correct_template(self):
        self.client.login(**self.USER_DATA)
        customer_representative = CustomerRepresentative.objects.first()

        response = self.client.get(reverse('edit_customer_representative',
                                           kwargs={'customer_id': customer_representative.customer.id,
                                                   'pk': customer_representative.pk}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer_representatives/customer_representative_edit.html')

    def test_get__when_user_is_not_logged__expect_to_redirect(self):
        customer_representative = CustomerRepresentative.objects.first()

        response = self.client.get(reverse('edit_customer_representative',
                                           kwargs={'customer_id': customer_representative.customer.id,
                                                   'pk': customer_representative.pk}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                             f'/accounts/login/?next=/customers/{customer_representative.customer.pk}/customer_representative/{customer_representative.pk}/')

    def test_post__when_data_is_correct__expect_to_update(self):
        self.client.login(**self.USER_DATA)

        customer_representative = CustomerRepresentative.objects.first()

        data = {
            'first_name': 'upd_name',
            'last_name': 'test_last',
            'email_address': 'upd@upd.com',
            'phone_number': '12345',
        }

        response = self.client.post(reverse('edit_customer_representative',
                                            kwargs={'customer_id': customer_representative.customer.id,
                                                    'pk': customer_representative.pk}), data)

        customer_representative.refresh_from_db()
        self.assertEqual(data['first_name'], customer_representative.first_name)
        self.assertEqual(data['last_name'], customer_representative.last_name)
        self.assertEqual(data['email_address'], customer_representative.email_address)
        self.assertEqual(data['phone_number'], customer_representative.phone_number)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('customer_detail', kwargs={'pk': customer_representative.customer.id}))
