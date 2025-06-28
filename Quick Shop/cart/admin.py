from django.contrib import admin
from cart.models import Cart, Order

# Register your models here.
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'item', 'color_variant', 'size_variant', 'quantity', 'purchased', 'total_price', 'variation_total_price', 'created_date', 'update_date']
admin.site.register(Cart, CartAdmin)

class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user',  'ordered', 'payment_id', 'order_id', 'payment_method', 'total_items', 'totals_price', 'created_date', 'update_date']
admin.site.register(Order, OrderAdmin)