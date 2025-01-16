from django.test import SimpleTestCase
from django.urls import reverse, resolve
from account import views
from django.contrib.auth import views as auth_views

class TestUrls(SimpleTestCase):

    def test_register_url(self):
        url = reverse('register')
        self.assertEqual(resolve(url).func, views.register)

    def test_email_verification_url(self):
        url = reverse('email-verification', args=['uidb64', 'token'])
        self.assertEqual(resolve(url).func, views.email_verification)

    def test_email_verification_sent_url(self):
        url = reverse('email-verification-sent')
        self.assertEqual(resolve(url).func, views.email_verification_sent)

    def test_email_verification_success_url(self):
        url = reverse('email-verification-success')
        self.assertEqual(resolve(url).func, views.email_verification_success)

    def test_email_verification_failed_url(self):
        url = reverse('email-verification-failed')
        self.assertEqual(resolve(url).func, views.email_verification_failed)

    def test_my_login_url(self):
        url = reverse('my-login')
        self.assertEqual(resolve(url).func, views.my_login)

    def test_user_logout_url(self):
        url = reverse('user-logout')
        self.assertEqual(resolve(url).func, views.user_logout)

    def test_dashboard_url(self):
        url = reverse('dashboard')
        self.assertEqual(resolve(url).func, views.dashboard)

    def test_profile_management_url(self):
        url = reverse('profile-management')
        self.assertEqual(resolve(url).func, views.profile_management)

    def test_delete_account_url(self):
        url = reverse('delete-account')
        self.assertEqual(resolve(url).func, views.delete_account)

    def test_reset_password_url(self):
        url = reverse('reset_password')
        self.assertEqual(resolve(url).func.view_class, auth_views.PasswordResetView)

    def test_reset_password_sent_url(self):
        url = reverse('password_reset_done')
        self.assertEqual(resolve(url).func.view_class, auth_views.PasswordResetDoneView)

    def test_reset_password_confirm_url(self):
        url = reverse('password_reset_confirm', args=['uidb64', 'token'])
        self.assertEqual(resolve(url).func.view_class, auth_views.PasswordResetConfirmView)

    def test_reset_password_complete_url(self):
        url = reverse('password_reset_complete')
        self.assertEqual(resolve(url).func.view_class, auth_views.PasswordResetCompleteView)

    def test_manage_shipping_url(self):
        url = reverse('manage-shipping')
        self.assertEqual(resolve(url).func, views.manage_shipping)

    def test_track_orders_url(self):
        url = reverse('track-orders')
        self.assertEqual(resolve(url).func, views.track_orders)
