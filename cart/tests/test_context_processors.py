from django.test import TestCase, RequestFactory
from cart.context_processors import cart as cart_context
from django.contrib.sessions.middleware import SessionMiddleware


class CartContextProcessorTest(TestCase):

    def setUp(self):
        """
        Sets up a request with a session for testing the context processor.
        """
        self.factory = RequestFactory()
        self.request = self.factory.get('/')

        # Add a session to the request
        middleware = SessionMiddleware(lambda req: None)  # Required get_response argument
        middleware.process_request(self.request)
        self.request.session.save()

    def test_cart_context_processor(self):
        """
        Test that the cart context processor adds a 'cart' key to the context.
        """
        context = cart_context(self.request)
        self.assertIn('cart', context)
        self.assertEqual(len(context['cart']), 0)  # Verify that the cart is initially empty

