from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from account.token import user_tokenizer_generate
from payment.models import ShippingAddress, OrderItem
from unittest.mock import patch

class AccountViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='testuser@example.com', password='password12345')

    # Test register view
    def test_register_view_get(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/registration/register.html')

    def test_register_view_post_valid(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password1': 'StrongPassword12345!',
            'password2': 'StrongPassword12345!',
        })
        self.assertRedirects(response, reverse('email-verification-sent'))
        self.assertTrue(User.objects.filter(username='newuser').exists())

    # Test email verification
    def test_email_verification_success(self):
        self.user.is_active = False
        self.user.save()
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        token = user_tokenizer_generate.make_token(self.user)

        response = self.client.get(reverse('email-verification', args=[uid, token]))
        self.assertRedirects(response, reverse('email-verification-success'))
        self.user.refresh_from_db()
        self.assertTrue(self.user.is_active)

    def test_email_verification_failure(self):
        uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        invalid_token = 'invalid-token'

        # Debugging reverse function
        print("Reverse URL for 'email-verification-failed':", reverse('email-verification-failed'))

        response = self.client.get(reverse('email-verification', args=[uid, invalid_token]))
        self.assertRedirects(response, reverse('email-verification-failed'))  # Verify redirect to failure page

    # Test login view
    def test_login_view_get(self):
        response = self.client.get(reverse('my-login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/my-login.html')

    def test_login_view_post_valid(self):
        response = self.client.post(reverse('my-login'), {
            'username': 'testuser',
            'password': 'password12345'
        })
        self.assertRedirects(response, reverse('dashboard'))

    def test_login_view_post_invalid(self):
        response = self.client.post(reverse('my-login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/my-login.html')

    # Test logout view
    def test_logout_view(self):
        self.client.login(username='testuser', password='password12345')
        response = self.client.get(reverse('user-logout'))
        self.assertRedirects(response, reverse('store'))

    # Test dashboard view
    def test_dashboard_view(self):
        self.client.login(username='testuser', password='password12345')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/dashboard.html')

    # Test profile management
    def test_profile_management_view_get(self):
        self.client.login(username='testuser', password='password12345')
        response = self.client.get(reverse('profile-management'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/profile-management.html')

    def test_profile_management_view_post_valid(self):
        self.client.login(username='testuser', password='password12345')
        response = self.client.post(reverse('profile-management'), {
            'username': 'updateduser',
            'email': 'updateduser@example.com',
            'old_password': 'password12345',
            'new_password1': 'NewStrongPassword123!',
            'new_password2': 'NewStrongPassword123!',
        })
        self.assertRedirects(response, reverse('dashboard'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.username, 'updateduser')

    # Test delete account
    def test_delete_account_view(self):
        self.client.login(username='testuser', password='password12345')
        response = self.client.post(reverse('delete-account'))
        self.assertRedirects(response, reverse('store'))
        self.assertFalse(User.objects.filter(username='testuser').exists())

    # Test manage shipping
    def test_manage_shipping_view_get(self):
        self.client.login(username='testuser', password='password12345')
        response = self.client.get(reverse('manage-shipping'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/manage_shipping.html')

    # Test track orders
    def test_track_orders_view(self):
        self.client.login(username='testuser', password='password12345')
        response = self.client.get(reverse('track-orders'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account/track-orders.html')


