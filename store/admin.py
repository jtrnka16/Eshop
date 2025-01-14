from django.contrib import admin
from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')  # Display the name and parent category in the admin list view
    prepopulated_fields = {"slug": ("name",)}  # Automatically generate the slug field based on the name
    list_filter = ('parent',)  # Filtering by parent category
    search_fields = ('name',)  # Search by name


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')  # Display the name and category in the admin list view
    prepopulated_fields = {"slug": ("name",)}  # Automatically generate the slug field based on the name
    list_filter = ('category',)  # Filtering by category
    search_fields = ('name',)  # Search by name
