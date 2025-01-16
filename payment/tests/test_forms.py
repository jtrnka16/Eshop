from django.test import TestCase
from payment.forms import ShippingForm


class TestShippingForm(TestCase):

    def test_shipping_form_valid_data(self):
        """
        Test that the form is valid when provided with correct data.
        """
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
        """
        Test that the form is invalid when provided with incorrect or missing data.
        Checks appropriate errors are raised for invalid fields.
        """
        form = ShippingForm(data={
            'full_name': '',  # Missing full_name
            'email': 'not-an-email',  # Invalid email format
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
        """
        Test that the 'user' field is excluded from the form.
        """
        form = ShippingForm()
        self.assertNotIn('user', form.fields)  # 'user' should not be part of the form
