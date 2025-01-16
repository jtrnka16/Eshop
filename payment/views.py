from django.shortcuts import render
from django.http import JsonResponse
from django.core.mail import send_mail
from django.conf import settings

from store.models import Product
from .models import ShippingAddress, Order, OrderItem
from cart.cart import Cart


def checkout(request):
    """
    Renders the checkout page.
    If the user is authenticated, pre-fill the form with their shipping address if available.
    """
    if request.user.is_authenticated:
        try:
            # Authenticated users with shipping information
            shipping_address = ShippingAddress.objects.get(user=request.user.id)
            context = {'shipping': shipping_address}
            return render(request, 'payment/checkout.html', context=context)
        except ShippingAddress.DoesNotExist:
            # Authenticated users with no shipping information
            return render(request, 'payment/checkout.html')

    # For unauthenticated users
    return render(request, 'payment/checkout.html')


def payment_success(request):
    """
    Clears the shopping cart and renders the payment success page.
    """
    for key in list(request.session.keys()):
        if key == 'session_key':
            del request.session[key]

    return render(request, 'payment/payment_success.html')


def payment_failed(request):
    """
    Renders the payment failed page.
    """
    return render(request, 'payment/payment_failed.html')


def complete_order(request):
    """
    Handles order completion, processes payment details, creates order records,
    and sends confirmation emails to users.
    """
    if request.POST.get('action') == 'post':
        # Retrieve form data
        name = request.POST.get('name')
        email = request.POST.get('email')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zipcode = request.POST.get('zipcode')

        # Construct the shipping address
        shipping_address = f"{address1}\n{address2}\n{city}\n{state}\n{zipcode}"

        # Get shopping cart and total cost
        cart = Cart(request)
        total_cost = cart.get_total()

        # Order creation variations
        product_list = []

        # 1) Authenticated users
        if request.user.is_authenticated:
            order = Order.objects.create(
                full_name=name,
                email=email,
                shipping_address=shipping_address,
                amount_paid=total_cost,
                user=request.user
            )
            order_id = order.pk

            for item in cart:
                OrderItem.objects.create(
                    order_id=order_id,
                    product=item['product'],
                    quantity=item['qty'],
                    price=item['price'],
                    user=request.user
                )
                product_list.append(item['product'])

        # 2) Guest users
        else:
            order = Order.objects.create(
                full_name=name,
                email=email,
                shipping_address=shipping_address,
                amount_paid=total_cost
            )
            order_id = order.pk

            for item in cart:
                OrderItem.objects.create(
                    order_id=order_id,
                    product=item['product'],
                    quantity=item['qty'],
                    price=item['price']
                )
                product_list.append(item['product'])

        # Send confirmation email
        all_products = product_list
        send_mail(
            'Order received',
            f"Hello!\n\nThank you for your order!\n\n"
            f"Please see your order details:\n\n{all_products}\n\n"
            f"Total paid: ${cart.get_total()}",
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False
        )

    # Respond with success
    order_success = True
    response = JsonResponse({'order_success': order_success})
    return response



