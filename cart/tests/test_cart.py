from django.test import TestCase, RequestFactory
from django.contrib.sessions.middleware import SessionMiddleware
from cart.cart import Cart
from store.models import Product


class CartTest(TestCase):

    def setUp(self):
        """
        Sets up test data and initializes a Cart instance.
        Creates a request with a session and two test products.
        """
        self.factory = RequestFactory()
        self.request = self.factory.get('/')

        # Attach a session to the request
        middleware = SessionMiddleware(lambda req: None)
        middleware.process_request(self.request)
        self.request.session.save()

        # Create products for testing
        self.product1 = Product.objects.create(name="Product 1", price=50.0, stock=10)
        self.product2 = Product.objects.create(name="Product 2", price=100.0, stock=5)

        # Initialize Cart with the request
        self.cart = Cart(self.request)

    def test_cart_initialization(self):
        """
        Test cart initialization for a new user.
        """
        self.assertEqual(len(self.cart), 0)  # Cart should be empty
        self.assertEqual(self.cart.cart, {})  # Cart data should be an empty dictionary

    def test_add_new_product(self):
        """
        Test adding a new product to the cart.
        """
        self.cart.add(self.product1, 2)
        self.assertEqual(len(self.cart), 2)  # Quantity should be 2
        self.assertIn(str(self.product1.id), self.cart.cart)  # Product should exist in the cart

    def test_update_existing_product_quantity(self):
        """
        Test updating the quantity of an existing product in the cart.
        """
        self.cart.add(self.product1, 2)
        self.cart.add(self.product1, 5)  # Update quantity to 5
        self.assertEqual(self.cart.cart[str(self.product1.id)]['qty'], 5)

    def test_delete_product(self):
        """
        Test deleting a product from the cart.
        """
        self.cart.add(self.product1, 2)
        self.cart.delete(self.product1.id)
        self.assertEqual(len(self.cart), 0)  # Cart should be empty
        self.assertNotIn(str(self.product1.id), self.cart.cart)  # Product should no longer exist in the cart

    def test_update_product_quantity(self):
        """
        Test updating the quantity of a product in the cart.
        """
        self.cart.add(self.product1, 2)
        self.cart.update(self.product1.id, 10)  # Update quantity to 10
        self.assertEqual(self.cart.cart[str(self.product1.id)]['qty'], 10)

    def test_cart_length(self):
        """
        Test the total quantity of items in the cart.
        """
        self.cart.add(self.product1, 2)
        self.cart.add(self.product2, 3)
        self.assertEqual(len(self.cart), 5)  # Total quantity should be 5 (2 + 3)

    def test_cart_iteration(self):
        """
        Test iterating over the items in the cart.
        """
        self.cart.add(self.product1, 2)
        self.cart.add(self.product2, 3)

        items = list(self.cart)
        self.assertEqual(len(items), 2)  # There should be 2 different products

        item1 = items[0]
        self.assertEqual(item1['product'], self.product1)
        self.assertEqual(item1['qty'], 2)
        self.assertEqual(item1['total'], self.product1.price * 2)  # Total price for product1

    def test_cart_total(self):
        """
        Test the total price of items in the cart.
        """
        self.cart.add(self.product1, 2)
        self.cart.add(self.product2, 3)
        total = self.cart.get_total()
        expected_total = (self.product1.price * 2) + (self.product2.price * 3)
        self.assertEqual(total, expected_total)  # Total should match the expected sum

