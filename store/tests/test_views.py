from django.test import TestCase
from django.urls import reverse
from store.models import Category, Product
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io


def get_test_image():
    """
    Creates a red test image for use in tests.

    Returns:
        A red JPEG image file.
    """
    img = Image.new("RGB", (100, 100), color="red")
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="JPEG")
    img_bytes.seek(0)
    return SimpleUploadedFile(name="test_image.jpg", content=img_bytes.read(), content_type="image/jpeg")


class StoreViewTest(TestCase):
    """
    Test suite for the store view.
    """

    def setUp(self):
        """
        Sets up test data for the store view.
        Creates a category and a product for testing.
        """
        self.category = Category.objects.create(name="Electronics", slug="electronics")
        self.product = Product.objects.create(
            name="Phone",
            category=self.category,
            slug="phone",
            price=100.0,
            stock=5,
            image=get_test_image()
        )

    def test_store_view_status_code(self):
        """
        Tests that the store view returns a 200 status code.
        """
        url = reverse('store')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_store_view_contains_products(self):
        """
        Tests that the store view contains the created product.
        """
        url = reverse('store')
        response = self.client.get(url)
        self.assertContains(response, "Phone")


class ProductInfoViewTest(TestCase):
    """
    Test suite for the product info view.
    """

    def setUp(self):
        """
        Sets up test data for the product info view.
        Creates a category and a product for testing.
        """
        self.category = Category.objects.create(name="Electronics", slug="electronics")
        self.product = Product.objects.create(
            name="Phone",
            category=self.category,
            slug="phone",
            price=100.0,
            stock=5,
            image=get_test_image()
        )

    def test_product_info_view_status_code(self):
        """
        Tests that the product info view returns a 200 status code.
        """
        url = reverse('product-info', args=['phone'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_product_info_view_context(self):
        """
        Tests that the product info view provides the correct context data.
        """
        url = reverse('product-info', args=['phone'])
        response = self.client.get(url)
        self.assertEqual(response.context['product'], self.product)
        self.assertTrue(response.context['in_stock'])
