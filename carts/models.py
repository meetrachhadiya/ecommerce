from django.db import models
from base.models import BaseModel
from accounts.models import User
from products.models import (
    Coupon,
    Product,
    SizeVariant,
) 

# Create your models here.

class Cart(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return (self.user.email + "'s cart")
    
    def get_cart_counter(self):
        quantity = 0
        for cart_item in self.cart_items.all():
            quantity += cart_item.quantity
        return quantity

    def get_cart_total(self):
        cart_items = self.cart_items.all()
        price = []
        for cart_item in cart_items:
            price.append(cart_item.price)
        
        if self.coupon:
            return sum(price) - self.coupon.coupon_discount_price
        return sum(price)

class CartItems(BaseModel):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    # color_variant = models.ForeignKey(ColorVariant, on_delete=models.CASCADE)
    size_variant = models.ForeignKey(SizeVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.FloatField(default=0)

    def __str__(self):
        return (self.cart.user.email + "'s cart")

    def save(self, *args, **kwargs):
        self.price = self.product.get_product_price(self.size_variant.size)*self.quantity
        super(CartItems, self).save(*args, **kwargs)

    class Meta:
        unique_together = ["cart","product","size_variant"]