from django.test import TestCase, Client
from django.urls import reverse
from store.models import Product
from django.core.files.uploadedfile import SimpleUploadedFile


class CartViewTest(TestCase):

    def setUp(self):
        """
        Sets up test data for cart view tests.
        Creates a product with a test image.
        """
        self.client = Client()
        self.product = Product.objects.create(
            name="Test Product",
            price=10.0,
            stock=20,
            slug="test-product",
            image=SimpleUploadedFile(
                name="test_image.jpg",
                content=b"file_content",
                content_type="image/jpeg"
            ),
        )

    def test_cart_summary_view(self):
        """
        Test displaying the cart overview page.
        """
        url = reverse('cart-summary')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'cart/cart-summary.html')

    def test_cart_add_view(self):
        """
        Test adding a product to the cart.
        """
        url = reverse('cart-add')
        response = self.client.post(url, {
            'action': 'post',
            'product_id': self.product.id,
            'product_quantity': 2,
        })
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(response.content, {'qty': 2})

    def test_cart_delete_view(self):
        """
        Test removing a product from the cart.
        """
        # Add the product to the cart first
        self.client.post(reverse('cart-add'), {
            'action': 'post',
            'product_id': self.product.id,
            'product_quantity': 2,
        })

        # Then remove the product from the cart
        url = reverse('cart-delete')
        response = self.client.post(url, {
            'action': 'post',
            'product_id': self.product.id,
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('qty', response.json())
        self.assertIn('total', response.json())

    def test_cart_update_view(self):
        """
        Test updating the quantity of a product in the cart.
        """
        # Add the product to the cart first
        self.client.post(reverse('cart-add'), {
            'action': 'post',
            'product_id': self.product.id,
            'product_quantity': 2,
        })

        # Update the product quantity
        url = reverse('cart-update')
        response = self.client.post(url, {
            'action': 'post',
            'product_id': self.product.id,
            'product_quantity': 5,
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn('qty', response.json())
        self.assertIn('total', response.json())





