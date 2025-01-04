from django.db import models

from django.contrib.auth.models import User

from store.models import Product

class ShippingAddress(models.Model):

    full_name = models.CharField(max_length=255)

    email = models.EmailField(max_length=255)

    address = models.CharField(max_length=300)

    address2 = models.CharField(max_length=300)

    city = models.CharField(max_length=255)

    state = models.CharField(max_length=255, null=True, blank=True) #Optional

    zipcode = models.CharField(max_length=10, null=True, blank=True) #Optional

    #FK

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True) # Authenticated / Not Authenticated

    class Meta:

        verbose_name_plural = "Shipping Address"

    def __str__(self):
        return 'Shipping Address - ' + str(self.id)

class Order(models.Model):

    full_name = models.CharField(max_length=300)

    email = models.EmailField(max_length=255)

    shipping_address = models.TextField(max_length=1000)

    amount_paid = models.DecimalField(max_digits=8, decimal_places=2)

    date_ordered = models.DateTimeField(auto_now_add=True)

    # FK

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):

        return 'Order - #' + str(self.id)

class OrderItem(models.Model):

    # FK ->

    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)

    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)

    quantity = models.PositiveIntegerField(default=1)

    price = models.DecimalField(max_digits=8, decimal_places=2)

    # FK

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):

        return 'Order - #' + str(self.id)