from django.test import TestCase
from payment.forms import ShippingForm
from payment.models import ShippingAddress


class TestShippingForm(TestCase):

    def test_shipping_form_valid_data(self):
        form = ShippingForm(data={
            'full_name': 'John Doe',
            'email': 'johndoe@example.com',
            'address': '123 Main Street',
            'address2': 'Apt 4B',
            'city': 'New York',
            'state': 'NY',
            'zipcode': '10001'
        })
        self.assertTrue(form.is_valid())  # Form should be valid with correct data

    def test_shipping_form_invalid_data(self):
        form = ShippingForm(data={
            'full_name': '',  # Missing full_name
            'email': 'not-an-email',  # Invalid email
            'address': '',
            'address2': '',
            'city': '',
            'state': '',
            'zipcode': ''
        })
        self.assertFalse(form.is_valid())  # Form should be invalid
        self.assertIn('full_name', form.errors)  # Error for missing full_name
        self.assertIn('email', form.errors)  # Error for invalid email

    def test_shipping_form_excluded_user_field(self):
        form = ShippingForm()
        self.assertNotIn('user', form.fields)  # 'user' should not be part of the form
