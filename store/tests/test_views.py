from django.test import TestCase
from django.urls import reverse
from store.models import Category, Product
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io

# Vytvoření reálného obrázku pro testy
def get_test_image():
    img = Image.new("RGB", (100, 100), color="red")
    img_bytes = io.BytesIO()
    img.save(img_bytes, format="JPEG")
    img_bytes.seek(0)
    return SimpleUploadedFile(name="test_image.jpg", content=img_bytes.read(), content_type="image/jpeg")

class StoreViewTest(TestCase):
    def setUp(self):
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
        url = reverse('store')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_store_view_contains_products(self):
        url = reverse('store')
        response = self.client.get(url)
        self.assertContains(response, "Phone")


class ProductInfoViewTest(TestCase):
    def setUp(self):
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
        url = reverse('product-info', args=['phone'])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_product_info_view_context(self):
        url = reverse('product-info', args=['phone'])
        response = self.client.get(url)
        self.assertEqual(response.context['product'], self.product)
        self.assertTrue(response.context['in_stock'])

