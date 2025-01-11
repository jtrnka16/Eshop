from django.db import models
from django.urls import reverse
from PIL import Image



class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='subcategories'
    )

    class Meta:
        verbose_name_plural = "Categories"   # defining the plural model name

    def __str__(self):
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' > '.join(full_path)

    def get_absolute_url(self):
        return reverse("list-category", args=[self.slug])

class Product(models.Model):
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)  # for optional information
    slug = models.SlugField(max_length=255)
    price = models.FloatField()
    stock = models.IntegerField()
    image = models.ImageField(upload_to="images/", blank=True)

    class Meta:
        verbose_name_plural = "Products"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("product-info", args=[self.slug])

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            img = Image.open(self.image.path)

            # Maxim size of image
            output_size = (300, 300)
            img.thumbnail(output_size)

            # Saving image
            img.save(self.image.path)

    def is_in_stock(self):
        """
        Returns True if the product stock is greater than 0, otherwise False.
        """
        return self.stock > 0

