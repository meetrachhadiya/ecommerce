from django.shortcuts import render
from accounts.models import User
from carts.models import Cart
from products.models import Category, Product, SizeVariant
# Create your views here.

def index(request):
    context = {'products' : Product.objects.all()}
    return render(request, 'home/index.html', context)

def search(request):
    products = Product.objects.all()
    categories = Category.objects.all()
    sizes = SizeVariant.objects.all()  # Query all size variants

    # Filtering by categories
    selected_categories = request.GET.getlist('categories[]')
    if selected_categories:
        products = products.filter(product_category__uid__in=selected_categories)

    # Filtering by name
    search_query = request.GET.get('name')
    if search_query:
        products = products.filter(product_name__icontains=search_query)

    # Filtering by minimum rating
    min_rating = request.GET.get('min_rating')
    if min_rating:
        products = products.filter(product_rating__gte=min_rating)

    # Filtering by new products
    if request.GET.get('new_products'):
        products = products.filter(is_new_product=True)

    # Filtering by products with discounts
    if request.GET.get('has_discounts'):
        products = products.filter(product_discount_price__isnull=False)

    # Filtering by size variant
    selected_sizes = request.GET.getlist('sizes[]')
    if selected_sizes:
        products = products.filter(size_variant__in=selected_sizes)

    context = {
        'products': products, 
        'categories': categories,
        'selected_categories': selected_categories,
        'selected_sizes': selected_sizes,  # Include selected_sizes in the context,
        'sizes': sizes,  # Pass sizes in the context
    }
    return render(request, 'home/search.html', context)

def temp(request):
    return render(request,'temp.html')