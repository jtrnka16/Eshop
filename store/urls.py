from django.urls import path
from . import views


urlpatterns = [
    # Main page
    path('', views.store, name='store'),
    # Product
    path('product/<slug:product_slug>', views.product_info, name='product-info'),
    # Category
    path('search/<slug:category_slug>', views.list_category, name='list-category'),

]