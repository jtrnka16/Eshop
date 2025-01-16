from django.contrib import admin
from .models import ShippingAddress, Order, OrderItem


class OrderAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'full_name', 'user', 'amount_paid', 'status', 'date_ordered')  # Fields to display
    list_filter = ('user', 'full_name', 'status', 'date_ordered')  # Fields for filtering
    search_fields = ('user__username', 'user__email', 'full_name')  # Fields for searching
    readonly_fields = ('date_ordered',)  # Fields marked as read-only


class ShippingAddressAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'full_name', 'city', 'state', 'user', 'email')  # Fields to display
    list_filter = ('city', 'state', 'user')  # Fields for filtering
    search_fields = ('full_name', 'city', 'state', 'user__username', 'user__email')  # Fields for searching


class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'order', 'user', 'product', 'quantity', 'price')  # Fields to display
    list_filter = ('order', 'user', 'product')  # Fields for filtering
    search_fields = ('order__id', 'user__username', 'user__email', 'product__name')  # Fields for searching


# Register models in the admin interface
admin.site.register(ShippingAddress, ShippingAddressAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem, OrderItemAdmin)

