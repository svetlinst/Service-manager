from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from service_manager.customers.models import Customer, CustomerRepresentative
from service_manager.master_data.models import CustomerType

UserModel = get_user_model()


class CreateCustomerRepresentativeTests(TestCase):
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

    def test_get__when_user_is_logged__expect_correct_template(self):
        self.client.login(**self.USER_DATA)

        customer = Customer.objects.first()

        response = self.client.get(
            reverse('create_customer_representative', kwargs={'customer_id': customer.id}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer_representatives/customer_representatives_create.html')
        self.assertIn('customer', response.context)
        self.assertEqual(customer, response.context['customer'])

    def test_get__when_user_is_not_logged__expect_to_redirect(self):
        customer = Customer.objects.first()

        response = self.client.get(
            reverse('create_customer_representative', kwargs={'customer_id': customer.id}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                             f'/accounts/login/?next=/customers/{customer.pk}/customer_representative/create/')

    def test_post__when_the_data_is_valid__expect_to_create(self):
        self.client.login(**self.USER_DATA)

        customer = Customer.objects.first()
        data = {
            # 'customer': customer.pk,
            'first_name': 'John',
            'last_name': 'Doe',
            'email_address': 'john@doe.com',
            'phone_number': '12345678900',
        }

        response = self.client.post(reverse('create_customer_representative', kwargs={'customer_id': customer.pk}),
                                    data)

        self.assertEqual(response.status_code, 302)
        customer_representatives = CustomerRepresentative.objects.all()
        self.assertEqual(len(customer_representatives), 1)
        customer_representative = customer_representatives[0]
        self.assertEqual(customer_representative.first_name, data['first_name'])
        self.assertEqual(customer_representative.last_name, data['last_name'])
        self.assertEqual(customer_representative.email_address, data['email_address'])
        self.assertEqual(customer_representative.phone_number, data['phone_number'])
        self.assertEqual(customer_representative.customer, customer)
        self.assertRedirects(response, reverse('customer_detail', kwargs={'pk': customer.pk}))

    def test_post__when_data_is_incorrect__expect_not_to_save(self):
        self.client.login(**self.USER_DATA)

        customer = Customer.objects.first()
        data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email_address': 'john_doe',
            'phone_number': '12345678900',
        }

        response = self.client.post(reverse('create_customer_representative', kwargs={'customer_id': customer.pk}),
                                    data)

        customer_representatives = CustomerRepresentative.objects.all()
        self.assertEqual(len(customer_representatives), 0)
        self.assertFalse(response.context_data['form'].is_valid())
        self.assertEqual(response.status_code, 200)