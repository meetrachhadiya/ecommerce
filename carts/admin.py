from django.contrib import admin
from carts.models import (
    Cart,
    CartItems,
)

# Register your models here.

class CartItemsInline(admin.TabularInline):
    model = CartItems
    extra = 0

class CartAdmin(admin.ModelAdmin):
    inlines = [CartItemsInline]

class CartItemsAdmin(admin.ModelAdmin):
    list_display = ('cart', 'product', 'size_variant', 'quantity', 'price')

admin.site.register(Cart, CartAdmin)
admin.site.register(CartItems, CartItemsAdmin)