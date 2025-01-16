from django.test import SimpleTestCase
from django.urls import reverse, resolve
from cart.views import cart_summary, cart_add, cart_delete, cart_update


class CartURLTest(SimpleTestCase):

    def test_cart_summary_url(self):
        url = reverse('cart-summary')
        self.assertEqual(resolve(url).func, cart_summary)

    def test_cart_add_url(self):
        url = reverse('cart-add')
        self.assertEqual(resolve(url).func, cart_add)

    def test_cart_delete_url(self):
        url = reverse('cart-delete')
        self.assertEqual(resolve(url).func, cart_delete)

    def test_cart_update_url(self):
        url = reverse('cart-update')
        self.assertEqual(resolve(url).func, cart_update)
