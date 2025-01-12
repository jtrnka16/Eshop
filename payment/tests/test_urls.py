from django.test import SimpleTestCase
from django.urls import reverse, resolve
from payment import views


class TestPaymentUrls(SimpleTestCase):

    def test_checkout_url(self):
        url = reverse('checkout')
        self.assertEqual(resolve(url).func, views.checkout)

    def test_complete_order_url(self):
        url = reverse('complete-order')
        self.assertEqual(resolve(url).func, views.complete_order)

    def test_payment_success_url(self):
        url = reverse('payment_success')
        self.assertEqual(resolve(url).func, views.payment_success)

    def test_payment_failed_url(self):
        url = reverse('payment_failed')
        self.assertEqual(resolve(url).func, views.payment_failed)
