from django.test import TestCase
from store.models import Category, Product


class CategoryModelTest(TestCase):

    def setUp(self):
        """
        Creates a parent category and a child category.
        """
        self.parent_category = Category.objects.create(name="Electronics", slug="electronics")
        self.child_category = Category.objects.create(name="Phones", slug="phones", parent=self.parent_category)

    def test_category_creation(self):
        """
        Checks if the parent and child categories are created correctly.
        """
        self.assertEqual(self.parent_category.name, "Electronics")
        self.assertEqual(self.child_category.parent, self.parent_category)

    def test_category_str(self):
        """
        Test the string representation of a Category instance.
        """
        self.assertEqual(str(self.child_category), "Electronics > Phones")

    def test_category_absolute_url(self):
        """
        Test the get_absolute_url method of the Category model.
        """
        self.assertEqual(self.parent_category.get_absolute_url(), "/search/electronics")


class ProductModelTest(TestCase):

    def setUp(self):
        """
        Creates a category and a product.
        """
        self.category = Category.objects.create(name="Electronics", slug="electronics")
        self.product = Product.objects.create(
            category=self.category,
            name="Test Phone",
            slug="test-phone",
            price=999.99,
            stock=10
        )

    def test_product_creation(self):
        """
        Checks if the product is correctly associated with its category.
        """
        self.assertEqual(self.product.name, "Test Phone")
        self.assertEqual(self.product.category, self.category)

    def test_product_is_in_stock(self):
        """
        Checks if the method returns True when stock is greater than 0.
        """
        self.assertTrue(self.product.is_in_stock())

    def test_product_absolute_url(self):
        """
        Test the get_absolute_url method of the Product model.
        """
        self.assertEqual(self.product.get_absolute_url(), "/product/test-phone")
