from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import OrderItem
from store.models import Product


@receiver(post_save, sender=OrderItem)
def update_product_stock(sender, instance, created, **kwargs):
    """
    Signal handler to update product stock when a new OrderItem is created.

    Args:
        sender: The model class that triggered the signal (OrderItem).
        instance: The instance of the OrderItem that was saved.
        created: A boolean indicating if the instance was created (True) or updated (False).
        **kwargs: Additional keyword arguments.
    """
    if created:  # The signal is triggered only when a new OrderItem is created
        product = instance.product
        if product.stock >= instance.quantity:
            product.stock -= instance.quantity
            product.save()
        else:
            raise ValueError(f"Sorry, {product.name} is out-of-stock.")
