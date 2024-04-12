from django.db import models
from base.models import BaseModel
from accounts.models import User
from products.models import Product, SizeVariant
import uuid

# Create your models here.

class Order(BaseModel):
    uid = None
    user =  models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    order_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    name = models.CharField(max_length=200)
    phone_number = models.IntegerField(null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    pincode = models.IntegerField(null=True, blank=True)
    order_total = models.FloatField(null=True, blank=True)
    order_discount = models.FloatField(null=True, blank=True)
    order_coupon_code = models.CharField(max_length=100, null=True, blank=True)
    razorpay_payment_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_order_id = models.CharField(max_length=100, null=True, blank=True)
    razorpay_signature = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.user.email} {self.order_id}"

class OrderItems(BaseModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True, blank=True)
    size_variant = models.ForeignKey(SizeVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.FloatField(default=0)



