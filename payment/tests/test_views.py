from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from store.models import Product
from payment.models import ShippingAddress, Order, OrderItem
from cart.cart import Cart


class TestPaymentViews(TestCase):

    def setUp(self):
        self.client = Client()

        # Create a user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a product
        self.product = Product.objects.create(
            name='Test Product',
            price=50.00,
            stock=10
        )

        # Create a shipping address
        self.shipping_address = ShippingAddress.objects.create(
            user=self.user,
            full_name='Test User',
            email='testuser@example.com',
            address='123 Test Street',
            city='Test City',
            state='Test State',
            zipcode='12345'
        )

        # Mock session data for the cart
        session = self.client.session
        session['session_key'] = {
            str(self.product.id): {'price': '50.00', 'qty': 2}
        }
        session.save()

    def test_checkout_authenticated_with_shipping(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.shipping_address.full_name)

    def test_checkout_authenticated_without_shipping(self):
        self.shipping_address.delete()  # Remove shipping address
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Test User')

    def test_checkout_guest(self):
        response = self.client.get(reverse('checkout'))
        self.assertEqual(response.status_code, 200)

    def test_payment_failed(self):
        response = self.client.get(reverse('payment_failed'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'payment/payment_failed.html')

    def test_complete_order_authenticated_user(self):
        self.client.login(username='testuser', password='testpassword')
        data = {
            'action': 'post',
            'name': 'Test User',
            'email': 'testuser@example.com',
            'address1': '123 Test Street',
            'address2': '',
            'city': 'Test City',
            'state': 'Test State',
            'zipcode': '12345'
        }
        response = self.client.post(reverse('complete-order'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Order.objects.filter(user=self.user).exists())
        self.assertTrue(OrderItem.objects.filter(order__user=self.user).exists())

    def test_complete_order_guest_user(self):
        data = {
            'action': 'post',
            'name': 'Guest User',
            'email': 'guest@example.com',
            'address1': '456 Guest Lane',
            'address2': '',
            'city': 'Guest City',
            'state': 'Guest State',
            'zipcode': '67890'
        }
        response = self.client.post(reverse('complete-order'), data)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Order.objects.filter(email='guest@example.com').exists())
        self.assertTrue(OrderItem.objects.filter(order__email='guest@example.com').exists())



