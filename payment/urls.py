from django.urls import path
from . import views

# Define URL patterns for the payment app
urlpatterns = [
    # Checkout page
    path('checkout', views.checkout, name='checkout'),

    # Endpoint to complete an order
    path('complete-order', views.complete_order, name='complete-order'),

    # Payment success page
    path('payment-success/', views.payment_success, name='payment_success'),

    # Payment failed page
    path('payment-failed/', views.payment_failed, name='payment_failed'),
]
