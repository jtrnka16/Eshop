from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import OrderItem
from store.models import Product

@receiver(post_save, sender=OrderItem)
def update_product_stock(sender, instance, created, **kwargs):

    if created:  # The signal is only triggered when a new OrderItem is created
        product = instance.product
        if product.stock >= instance.quantity:
            product.stock -= instance.quantity
            product.save()
        else:
            raise ValueError(f"Sorry, {product.name} is out-of-stock.")