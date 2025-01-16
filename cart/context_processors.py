from .cart import Cart


def cart(request):
    """
    Context processor to include the cart in the template context.

    Args:
        request: The HTTP request object.

    Returns:
        dict: A dictionary containing the cart instance.
    """
    return {'cart': Cart(request)}
