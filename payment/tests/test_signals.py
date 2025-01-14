from django.test import TestCase
from payment.models import OrderItem
from store.models import Product


class TestUpdateProductStockSignal(TestCase):

    def setUp(self):
        """
        Sets up test data for the signal tests.
        Creates a product with an initial stock value.
        """
        self.product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            slug="test-product",
            price=100.0,  # Product price
            stock=10,  # Initial stock
        )

    def test_product_stock_reduction_on_order_item_creation(self):
        """
        Test that product stock is reduced correctly when an OrderItem is created.
        """
        # Create an order item with a specific quantity
        OrderItem.objects.create(
            product=self.product,
            quantity=3,  # Quantity to order
            price=self.product.price,  # Product price
        )

        # Reload the product from the database
        self.product.refresh_from_db()

        # Assert that the stock has been reduced correctly
        self.assertEqual(self.product.stock, 7)  # Initial stock 10 - quantity 3

    def test_product_stock_insufficient(self):
        """
        Test that creating an OrderItem with a quantity exceeding stock raises an error.
        """
        with self.assertRaises(ValueError):  # Expecting a ValueError
            OrderItem.objects.create(
                product=self.product,
                quantity=15,  # Quantity exceeds stock
                price=self.product.price,  # Product price
            )

        # Reload the product from the database
        self.product.refresh_from_db()

        # Ensure the stock remains unchanged
        self.assertEqual(self.product.stock, 10)  # Stock remains unchanged
