from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem

class OrderAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ('__str__', 'full_name', 'user', 'amount_paid', 'status', 'date_ordered')

    # Filtering by parent category
    list_filter = ('user', 'full_name', 'status', 'date_ordered')

    # Filtering by name
    search_fields = ('user__username', 'user__email', 'full_name')

    # Read-only fields in the detail view
    readonly_fields = ('date_ordered',)


class ShippingAddressAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ('__str__', 'full_name', 'city', 'state', 'user', 'email')

    # Fields to filter by
    list_filter = ('city', 'state', 'user')

    # Fields to search by
    search_fields = ('full_name', 'city', 'state', 'user__username', 'user__email')


class OrderItemAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ('__str__', 'order', 'user', 'product', 'quantity', 'price')

    # Fields to filter by
    list_filter = ('order', 'user', 'product')

    # Fields to search by
    search_fields = ('order__id', 'user__username', 'user__email', 'product__name')

# Registering models
admin.site.register(ShippingAddress, ShippingAddressAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)

