from django.db import models
from django.urls import reverse


class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)

    class Meta:
        verbose_name_plural = "Categories" #defining the plural model name

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("list-category", args=[self.slug])

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True) #for optional information
    slug = models.SlugField(max_length=255)
    price = models.FloatField()
    stock = models.IntegerField()
    image = models.ImageField(upload_to="images/", blank=True)

    class Meta:
        verbose_name_plural = "Products"  # defining the plural model name

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("product-info", args=[self.slug])

