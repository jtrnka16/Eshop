from django.test import TestCase
from payment.models import OrderItem
from store.models import Product


class TestUpdateProductStockSignal(TestCase):

    def setUp(self):
        # Create a product for testing
        self.product = Product.objects.create(
            name="Test Product",
            description="Test Description",
            slug="test-product",
            price=100.0,  # Product price
            stock=10,  # Initial stock
        )

    def test_product_stock_reduction_on_order_item_creation(self):
        # Create an order item
        order_item = OrderItem.objects.create(
            product=self.product,
            quantity=3,  # Quantity to order
            price=self.product.price,  # Provide price field
        )

        # Reload the product from the database
        self.product.refresh_from_db()

        # Check if the stock was reduced correctly
        self.assertEqual(self.product.stock, 7)  # Initial stock 10 - quantity 3

    def test_product_stock_insufficient(self):
        with self.assertRaises(ValueError):  # Expecting a ValueError
            OrderItem.objects.create(
                product=self.product,
                quantity=15,  # Quantity exceeds stock
                price=self.product.price,  # Provide price field
            )

        # Reload the product from the database
        self.product.refresh_from_db()

        # Ensure stock has not changed
        self.assertEqual(self.product.stock, 10)  # Stock remains unchanged
