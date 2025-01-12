from django.test import TestCase, RequestFactory
from cart.context_processors import cart as cart_context
from django.contrib.sessions.middleware import SessionMiddleware

class CartContextProcessorTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.request = self.factory.get('/')

        # Adding session to request
        middleware = SessionMiddleware(lambda req: None)  # Adding mandatory get_response argument
        middleware.process_request(self.request)
        self.request.session.save()

    def test_cart_context_processor(self):
        context = cart_context(self.request)
        self.assertIn('cart', context)
        self.assertEqual(len(context['cart']), 0)  # Verifying that cart is empty
