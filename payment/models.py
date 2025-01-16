from django.db import models
from django.contrib.auth.models import User
from store.models import Product


class ShippingAddress(models.Model):
    """Model representing a shipping address for a user."""

    full_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    address = models.CharField(max_length=300)
    address2 = models.CharField(max_length=300)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255, null=True, blank=True)  # Optional
    zipcode = models.CharField(max_length=10, null=True, blank=True)  # Optional

    # Foreign Key to user
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        verbose_name_plural = "Shipping Address"

    def __str__(self):
        """String representation of the ShippingAddress model."""
        return f"Shipping Address - {self.id}"


class Order(models.Model):
    """Model representing an order."""

    STATUS_CHOICES = [
        ('received', 'Received'),
        ('shipped', 'Shipped'),
        ('completed', 'Completed')
    ]

    full_name = models.CharField(max_length=300)
    email = models.EmailField(max_length=255)
    shipping_address = models.TextField(max_length=1000)
    amount_paid = models.DecimalField(max_digits=8, decimal_places=2)
    date_ordered = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='received'  # Default value for order
    )

    # Foreign Key to user
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        """String representation of the Order model."""
        return f"Order - #{self.id}"


class OrderItem(models.Model):
    """Model representing an item in an order."""

    # Foreign Keys
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)

    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=8, decimal_places=2)

    # Foreign Key to user
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"OrderItem - #{self.id}"
