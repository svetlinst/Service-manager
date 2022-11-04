from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from service_manager.customers.models import Customer, CustomerRepresentative
from service_manager.master_data.models import CustomerType

UserModel = get_user_model()


class DeleteCustomerRepresentativeView(TestCase):
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
            first_name='Fname',
            last_name='Lname',
            email_address='test@case.com',
            phone_number='988999880',
        )

    def test_get__when_the_user_is_logged__expect_correct_template(self):
        self.client.login(**self.USER_DATA)

        customer_representative = CustomerRepresentative.objects.first()

        response = self.client.get(reverse('delete_customer_representative',
                                           kwargs={'customer_id': customer_representative.customer.id,
                                                   'pk': customer_representative.pk}))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'customer_representatives/customer_representative_delete.html')

    def test_get__when_user_is_not_logged__expect_to_redirect(self):
        customer_representative = CustomerRepresentative.objects.first()

        response = self.client.get(reverse('delete_customer_representative',
                                           kwargs={'customer_id': customer_representative.customer.id,
                                                   'pk': customer_representative.pk}))

        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response,
                             f'/accounts/login/?next=/customers/{customer_representative.customer.pk}/customer_representative/delete/{customer_representative.pk}/')

    def test_post__expect_to_delete(self):
        self.client.login(**self.USER_DATA)

        customer_representative = CustomerRepresentative.objects.first()
        customer = customer_representative.customer

        response = self.client.post(reverse('delete_customer_representative',
                                           kwargs={'customer_id': customer.id,
                                                   'pk': customer_representative.pk}))

        customer_representative.refresh_from_db()
        self.assertFalse(customer_representative.active)
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('customer_detail', kwargs={'pk': customer.pk}))
