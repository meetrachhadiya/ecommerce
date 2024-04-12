
from django.shortcuts import render
from products.models import Product

# Create your views here.

def get_product(request, uid):
    product = Product.objects.get(uid=uid)

    product_rating = "i" * int(product.product_rating)
    context = {'product': product , 'product_rating': product_rating}

    if request.GET.get('size'):
        size = request.GET.get('size')
        price = product.get_product_price(size)
        context['selected_size'] = size
        context['updated_price'] = price

    return render(request, 'products/product.html', context)


    