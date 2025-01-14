from django.urls import path
from . import views

# Define URL patterns for the store app
urlpatterns = [
    # Main page displaying the store
    path('', views.store, name='store'),

    # Product details page
    path('product/<slug:product_slug>', views.product_info, name='product-info'),

    # Category search and filtering page
    path('search/<slug:category_slug>', views.list_category, name='list-category'),
]
