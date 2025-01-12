from django.test import SimpleTestCase
from django.urls import reverse, resolve
from store.views import store, list_category, product_info

class StoreURLTest(SimpleTestCase):
    def test_store_url_resolves(self):
        url = reverse('store')
        self.assertEqual(resolve(url).func, store)

    def test_list_category_url_resolves(self):
        url = reverse('list-category', args=['electronics'])
        self.assertEqual(resolve(url).func, list_category)

    def test_product_info_url_resolves(self):
        url = reverse('product-info', args=['test-phone'])
        self.assertEqual(resolve(url).func, product_info)
