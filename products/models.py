from django.db import models
from base.models import BaseModel
from django.db import models
from base.models import BaseModel
from django.utils.text import slugify

# Create your models here.

class Category(BaseModel):
    category_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    category_image = models.ImageField(upload_to="category", null=True, blank=True)

    def __str__(self):
        return self.category_name
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.category_name)
        super(Category, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.category_image.delete()
        super().delete(*args, **kwargs)

# class ColorVariant(BaseModel):
#     color = models.CharField(max_length=100)   
#     color_price = models.IntegerField(default=0)
#     def __str__(self):
#         return self.color

class SizeVariant(BaseModel):
    size = models.CharField(max_length=100)   
    size_price = models.IntegerField(default=0)
    def __str__(self):
        return self.size

class Product(BaseModel):
    product_name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True, null=True, blank=True)
    product_category = models.ForeignKey("Category", on_delete=models.CASCADE, related_name="products")
    product_price = models.FloatField()
    discount = models.IntegerField(default=0)
    product_discount_price = models.FloatField(null=True, blank=True)
    # color_variant = models.ManyToManyField(ColorVariant)
    size_variant = models.ManyToManyField(SizeVariant)
    product_description = models.TextField()
    is_new_product = models.BooleanField(default=False)
    product_total_review = models.IntegerField(null=True, blank=True)
    product_rating = models.IntegerField(default=0)
    product_total_order = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.product_name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.product_name)
        self.product_discount_price = self.product_price * (100 - self.discount)/100
        super(Product, self).save(*args, **kwargs)

    def get_product_price(self, size):
        return self.product_discount_price + SizeVariant.objects.get(size=size).size_price

class ProductImage(BaseModel):
    product = models.ForeignKey(Product , on_delete=models.CASCADE , related_name="product_images")
    product_image =  models.ImageField(upload_to="product")

    def __str__(self):
        return self.product.product_name
    
    def delete(self, *args, **kwargs):
        self.product_image.delete()
        super(ProductImage, self).delete(*args, **kwargs)

class Coupon(BaseModel):
    coupon_code = models.CharField(max_length=100)
    coupon_discount_price = models.FloatField()
    is_expired = models.BooleanField(default=False)
    minimum_amount = models.IntegerField()
    
    def __str__(self):
        return self.coupon_code
