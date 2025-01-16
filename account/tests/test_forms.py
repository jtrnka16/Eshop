from django.test import TestCase
from django.contrib.auth.models import User
from account.forms import CreateUserForm, LoginForm, UpdateUserForm


class CreateUserFormTest(TestCase):

    def test_valid_form(self):
        """
        Test that the form is valid with correct data and no duplicate email.
        """
        # Ensure no duplicate emails in the database
        User.objects.filter(email='testuser@example.com').delete()

        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'StrongPassword12345!',
            'password2': 'StrongPassword12345!',
        }
        form = CreateUserForm(data=form_data)
        self.assertTrue(form.is_valid())  # Form should be valid

    def test_invalid_duplicate_email(self):
        """
        Test that the form is invalid when the email is already in use.
        """
        User.objects.create_user(username='existinguser', email='testuser@example.com', password='password12345')

        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password1': 'password12345',
            'password2': 'password12345',
        }
        form = CreateUserForm(data=form_data)
        self.assertFalse(form.is_valid())  # Form should be invalid
        self.assertIn('email', form.errors)  # Email should have an error

    def test_invalid_email_too_long(self):
        """
        Test that the form is invalid when the email exceeds the maximum length.
        """
        form_data = {
            'username': 'testuser',
            'email': 'a' * 351 + '@example.com',  # 351 characters
            'password1': 'password12345',
            'password2': 'password12345',
        }
        form = CreateUserForm(data=form_data)
        self.assertFalse(form.is_valid())  # Form should be invalid
        self.assertIn('email', form.errors)  # Email should have an error


class LoginFormTest(TestCase):
    """
    Test suite for the LoginForm.
    """

    def setUp(self):
        """
        Sets up a user for testing login functionality.
        """
        self.user = User.objects.create_user(username='testuser', password='password12345')

    def test_valid_login(self):
        """
        Test that the form is valid with correct login credentials.
        """
        form_data = {'username': 'testuser', 'password': 'password12345'}
        form = LoginForm(data=form_data)
        self.assertTrue(form.is_valid())  # Form should be valid

    def test_invalid_login(self):
        """
        Test that the form is invalid with incorrect login credentials.
        """
        form_data = {'username': 'testuser', 'password': 'wrongpassword'}
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())  # Form should be invalid


class UpdateUserFormTest(TestCase):
    """
    Test suite for the UpdateUserForm.
    """

    def setUp(self):
        """
        Sets up a user for testing update functionality.
        """
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='password12345')

    def test_valid_update(self):
        """
        Test that the form is valid with correct update data.
        """
        form_data = {'username': 'updateduser', 'email': 'updateduser@example.com'}
        form = UpdateUserForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())  # Form should be valid

    def test_invalid_duplicate_email(self):
        """
        Test that the form is invalid when the updated email already exists.
        """
        User.objects.create_user(username='otheruser', email='conflict@example.com', password='password12345')

        form_data = {'username': 'updateduser', 'email': 'conflict@example.com'}
        form = UpdateUserForm(data=form_data, instance=self.user)
        self.assertFalse(form.is_valid())  # Form should be invalid
        self.assertIn('email', form.errors)  # Email should have an error

    def test_invalid_email_too_long(self):
        """
        Test that the form is invalid when the updated email exceeds the maximum length.
        """
        form_data = {'username': 'updateduser', 'email': 'a' * 351 + '@example.com'}
        form = UpdateUserForm(data=form_data, instance=self.user)
        self.assertFalse(form.is_valid())  # Form should be invalid
        self.assertIn('email', form.errors)  # Email should have an error

