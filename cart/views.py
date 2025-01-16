from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .cart import Cart
from store.models import Product


def cart_summary(request):
    """
    Renders the cart summary page, displaying the current cart contents.
    """
    cart = Cart(request)
    return render(request, 'cart/cart-summary.html', {'cart': cart})


def cart_add(request):
    """
    Adds a product to the cart.

    Handles AJAX POST requests to add a specified quantity of a product
    to the shopping cart.

    Returns:
        JsonResponse: Contains the quantity of the added product.
    """
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_quantity = int(request.POST.get('product_quantity'))

        # Retrieve the product or return 404 if not found
        product = get_object_or_404(Product, id=product_id)

        # Add product to the cart
        cart.add(product=product, product_qty=product_quantity)

        response = JsonResponse({'qty': product_quantity})
        return response


def cart_delete(request):
    """
    Deletes a product from the cart.

    Handles AJAX POST requests to remove a specified product from the cart.

    Returns:
        JsonResponse: Contains the updated cart quantity and total price.
    """
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))

        # Delete product from the cart
        cart.delete(product=product_id)

        cart_quantity = cart.__len__()
        cart_total = cart.get_total()

        response = JsonResponse({'qty': cart_quantity, 'total': cart_total})
        return response


def cart_update(request):
    """
    Updates the quantity of a product in the cart.

    Handles AJAX POST requests to modify the quantity of a specified product.

    Returns:
        JsonResponse: Contains the updated cart quantity and total price.
    """
    cart = Cart(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('product_id'))
        product_quantity = int(request.POST.get('product_quantity'))

        # Update product quantity in the cart
        cart.update(product=product_id, qty=product_quantity)

        cart_quantity = cart.__len__()
        cart_total = cart.get_total()

        response = JsonResponse({'qty': cart_quantity, 'total': cart_total})
        return response

