from decimal import Decimal
from store.models import Product


class Cart:

    def __init__(self, request):
        """
        Initializes the cart instance.

        Args:
            request: The HTTP request object, used to access the session.
        """
        self.session = request.session

        # Check for an existing session or create a new one
        cart = self.session.get('session_key')
        if 'session_key' not in request.session:
            cart = self.session['session_key'] = {}

        self.cart = cart

    def add(self, product, product_qty):
        """
        Adds or updates a product in the cart.

        Args:
            product: The product instance to add or update.
            product_qty: The quantity of the product to add.
        """
        product_id = str(product.id)

        if product_id in self.cart:
            self.cart[product_id]['qty'] = product_qty
        else:
            self.cart[product_id] = {'price': str(product.price), 'qty': product_qty}

        self.session.modified = True

    def delete(self, product):
        """
        Deletes a product from the cart.

        Args:
            product: The ID of the product to delete.
        """
        product_id = str(product)

        if product_id in self.cart:
            del self.cart[product_id]

        self.session.modified = True

    def update(self, product, qty):
        """
        Updates the quantity of a product in the cart.

        Args:
            product: The ID of the product to update.
            qty: The new quantity of the product.
        """
        product_id = str(product)

        if product_id in self.cart:
            self.cart[product_id]['qty'] = qty

        self.session.modified = True

    def __len__(self):
        """
        Returns the total number of items in the cart.

        Returns:
            int: The total quantity of items in the cart.
        """
        return sum(item['qty'] for item in self.cart.values())

    def __iter__(self):
        """
        Iterates over the items in the cart, adding product instances and
        calculating total prices for each item.

        Yields:
            dict: A dictionary containing product details, price, quantity, and total.
        """
        all_product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=all_product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total'] = item['price'] * item['qty']
            yield item

    def get_total(self):
        """
        Calculates the total cost of all items in the cart.

        Returns:
            Decimal: The total cost of the items in the cart.
        """
        return sum(Decimal(item['price']) * item['qty'] for item in self.cart.values())



