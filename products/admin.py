from django.contrib import admin
from products.models import (
    Category,
    Product,
    ProductImage,
    SizeVariant,
    Coupon,
)

# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
    readonly_fields = ['uid']

class ProductImageAdmin(admin.StackedInline):
    model = ProductImage

class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageAdmin]

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(ProductImage)
admin.site.register(SizeVariant)
admin.site.register(Coupon)