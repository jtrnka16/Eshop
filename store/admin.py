from django.contrib import admin

from . models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')  # Adding column for diplaying the parrent category
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ('parent',)  # Filtering by parent category
    search_fields = ('name',)  # Filtering by name

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')  # Adding column for diplaying the category
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ('category',)  # Filtering by  category
    search_fields = ('name',)  # Filtering by name