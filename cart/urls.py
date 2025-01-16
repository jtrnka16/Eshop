from django.urls import path
from . import views

# Define URL patterns for the cart app
urlpatterns = [
    # Display the cart summary
    path('', views.cart_summary, name='cart-summary'),

    # Add a product to the cart
    path('add/', views.cart_add, name='cart-add'),

    # Delete a product from the cart
    path('delete/', views.cart_delete, name='cart-delete'),

    # Update the quantity of a product in the cart
    path('update/', views.cart_update, name='cart-update'),
]
