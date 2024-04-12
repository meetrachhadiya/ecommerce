from django.contrib import admin
from orders.models import Order, OrderItems
# Register your models here.

# admin.site.register(RazorPayOrder)

class OrderItemsInline(admin.TabularInline):
    model = OrderItems
    extra = 0

class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemsInline]

admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItems)

