from django.db import models
from django.urls import reverse
from PIL import Image, UnidentifiedImageError


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
        verbose_name_plural = "Categories"  # Defining the plural model name

    def __str__(self):
        """
        Returns the full category path (including parent categories).
        """
        full_path = [self.name]
        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent
        return ' > '.join(reversed(full_path))

    def get_absolute_url(self):
        return reverse("list-category", args=[self.slug])


class Product(models.Model):
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)  # Optional description of the product
    slug = models.SlugField(max_length=255)
    price = models.FloatField()
    stock = models.IntegerField()
    image = models.ImageField(upload_to="images/", blank=True)

    class Meta:
        verbose_name_plural = "Products"  # Defining the plural model name

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("product-info", args=[self.slug])

    def save(self, *args, **kwargs):
        """
        Saves the product instance and processes the image if provided.
        Resizes the image to a maximum of 300x300 pixels.
        """
        super().save(*args, **kwargs)

        if self.image:
            try:
                img = Image.open(self.image.path)

                # Maximum size of the image
                output_size = (300, 300)
                img.thumbnail(output_size)

                # Save the resized image
                img.save(self.image.path)

            except UnidentifiedImageError:
                # Ignore the error if the image is invalid or mocked
                pass

    def is_in_stock(self):
        """
        Checks if the product is in stock.
        """
        return self.stock > 0


