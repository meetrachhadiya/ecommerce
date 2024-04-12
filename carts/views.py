from django.shortcuts import redirect, render
from django.http import HttpResponseBadRequest, HttpResponseRedirect, JsonResponse
from accounts.models import Address
from carts.models import Cart, CartItems
from products.models import (Product, SizeVariant, Coupon)
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.conf import settings
from orders.models import Order, OrderItems
import razorpay
# from django.core.urlresolvers import revers

# Create your views here.

@login_required(login_url='login')
def cart(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    if request.method == "POST":
        coupon_code = request.POST.get('coupon_code')
        try:
            coupon = Coupon.objects.get(coupon_code=coupon_code)
        except Exception as e:
            messages.warning(request, "Invalid Coupon!!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        if coupon.is_expired:
            messages.warning(request, "Coupon is Expired!!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        if cart.coupon:
            if cart.coupon == coupon:
                messages.warning(request, "Coupon is already applied!!")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
            else:
                messages.warning(request, "Another Coupon is applied!!")
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        if coupon.minimum_amount and coupon.minimum_amount > cart.get_cart_total():
            messages.warning(request, "Coupon is not applicable!!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        
        
        cart.coupon = coupon
        cart.save()
        messages.success(request, "Coupon Applied Successfully!!")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    
    # client = razorpay.Client(auth = (settings.KEY, settings.SECRET))
    # payment = client.order.create({
    #     'amount' : cart.get_cart_total() * 100,
    #     'currency' : 'INR',
    #     'payment_capture' : 1, 
    # })

    
    # print(payment)

    context = {'cart' : cart}
    return render(request, 'carts/cart.html', context)

@login_required(login_url="login")
def remove_coupon(request, uid):
    cart = Cart.objects.get(uid=uid)
    cart.coupon = None
    cart.save()
    messages.success(request, "Coupon in removed")
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required(login_url="login")
def add_to_cart(request, uid):
    product = Product.objects.get(uid=uid)

    cart, created = Cart.objects.get_or_create(user=request.user)
    
    size = request.GET.get('size')
    print(size)
    if size :
        size_variant = SizeVariant.objects.get(size=size)
    else:
        messages.warning(request, "select a size to continue")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    cart_item = CartItems.objects.filter(cart=cart, product=product, size_variant=size_variant)
    print(cart_item)
    if cart_item.exists():
        cart_item = cart_item.first()
        quantity =int(request.GET.get('quantity'))
        cart_item.quantity += quantity 
        cart_item.save()
    
    else:
        cart_items = CartItems.objects.create(cart=cart, product=product, size_variant=size_variant)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def buy_now(request, uid):
    product = Product.objects.get(uid=uid)

    cart, created = Cart.objects.get_or_create(user=request.user)
    
    size = request.GET.get('size')
    print(size)
    if size :
        size_variant = SizeVariant.objects.get(size=size)
    else:
        messages.warning(request, "select a size to continue")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    
    cart_item = CartItems.objects.filter(cart=cart, product=product, size_variant=size_variant)
    print(cart_item)
    if cart_item.exists():
        cart_item = cart_item.first()
        quantity =int(request.GET.get('quantity'))
        cart_item.quantity += quantity 
        cart_item.save()
    
    else:
        cart_items = CartItems.objects.create(cart=cart, product=product, size_variant=size_variant)

    return redirect('checkout')    

@login_required(login_url="login")
def remove_from_cart(request, uid):
    try:
        cart_items = CartItems.objects.get(uid=uid)
        cart_items.delete()
    except Exception as e:
        print(e)

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def update_quantity(request):
    if request.method == 'GET':
        cart_item_id = request.GET.get('cart_item_id')
        new_quantity = int(request.GET.get('quantity'))

        # Retrieve the CartItems object from the database
        cart_item = get_object_or_404(CartItems, uid = cart_item_id)

        # Update the quantity
        cart_item.quantity = new_quantity
        cart_item.save()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    return HttpResponseBadRequest('GET method not supported for updating quantity.')

@login_required(login_url="login")
def checkout(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    context = {'cart' : cart}

    return render(request, 'carts/checkout.html', context)


def continue_to_payment(request):
    if request.method == 'POST':
        selected_address_uid = request.POST.get('selected_address')
        if selected_address_uid:
            # Process the selected address ID
            selected_address = Address.objects.get(uid=selected_address_uid)
            # You can now use the selected address as needed, such as storing it in the session
            request.session['selected_address'] = selected_address_uid
            # Redirect the user to the payment page
            return redirect('payment')
        else:
            messages.warning(request, 'Please select a shipping address.')
            return redirect('checkout')
    else:
        # If the request method is not POST, redirect back to the checkout page
        return redirect('checkout')

@login_required(login_url="login")
def payment(request):
    cart = Cart.objects.get(user=request.user)
    context = {'cart' : cart}

    # Retrieve the selected address ID from the session
    selected_address_uid = request.session.get('selected_address')
    if selected_address_uid:
        selected_address = Address.objects.get(uid=selected_address_uid)
        # Render the payment page with the selected address
        # return render(request, 'cart/spayment.html', {'selected_address': selected_address})
    else:
        # If the selected address is not found in the session, redirect back to the checkout page
        messages.warning(request, 'Please select a shipping address.')
        return redirect('checkout')
    
    if request.method == "POST":
        if "payment_method" in request.POST:
            if request.POST["payment_method"] == "COD":
                if cart.coupon:
                    order = Order.objects.create(
                        user=request.user,
                        name=selected_address.name,
                        phone_number=selected_address.phone_number,
                        address=selected_address.address,
                        pincode=selected_address.pincode,
                        order_total=cart.get_cart_total(),
                        order_discount=cart.coupon.coupon_discount_price,
                        order_coupon_code=cart.coupon.coupon_code
                    )

                    for item in cart.cart_items.all:
                        OrderItems.objects.create(
                            order = order,
                            product = item.product,
                            size_variant = item.size_variant,
                            quantity = item.quantity,
                            price = item.price
                        )
                else:
                    order = Order.objects.create(
                        user=request.user,
                        name=selected_address.name,
                        phone_number=selected_address.phone_number,
                        address=selected_address.address,
                        pincode=selected_address.pincode,
                        order_total=cart.get_cart_total(), 
                    )

                for item in cart.cart_items.all():
                        OrderItems.objects.create(
                            order = order,
                            product = item.product,
                            size_variant = item.size_variant,
                            quantity = item.quantity,
                            price = item.price
                        )
                    
                cart.delete()
                return redirect('order-confirm')

            if request.POST["payment_method"] == "razorpay":
                print('razorpay')
                if cart.coupon:
                    order = Order.objects.create(
                        user=request.user,
                        name=selected_address.name,
                        phone_number=selected_address.phone_number,
                        address=selected_address.address,
                        pincode=selected_address.pincode,
                        order_total=cart.get_cart_total(),
                        order_discount=cart.coupon.coupon_discount_price,
                        order_coupon_code=cart.coupon.coupon_code,
                        razorpay_payment_id = request.POST["razorpay_payment_id"],
                        razorpay_order_id = request.POST["razorpay_order_id"],
                        razorpay_signature = request.POST["razorpay_signature"],
                    )
                else:
                    order = Order.objects.create(
                        user=request.user,
                        name=selected_address.name,
                        phone_number=selected_address.phone_number,
                        address=selected_address.address,
                        pincode=selected_address.pincode,
                        order_total=cart.get_cart_total(),
                        razorpay_payment_id = request.POST["razorpay_payment_id"],
                        razorpay_order_id = request.POST["razorpay_order_id"],
                        razorpay_signature = request.POST["razorpay_signature"],
                    )

                for item in cart.cart_items.all():
                        OrderItems.objects.create(
                            order = order,
                            product = item.product,
                            size_variant = item.size_variant,
                            quantity = item.quantity,
                            price = item.price
                        )   
                
                cart.delete()
                print("hiii")
                return JsonResponse(status = 302 , data = {'success' : '127.0.0.1:8000/order/confirm' })
                print("hiii")
                
    client = razorpay.Client(auth = (settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    payment = client.order.create({
        'amount' : cart.get_cart_total() * 100,
        'currency' : 'INR',
        'payment_capture' : 1, 
    })
    print(payment)
    context['payment'] = payment
    context['secret_key'] = settings.RAZORPAY_KEY_ID
        # messages.success(request, "Order Placed Successfully!!")
        # return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    return render(request, 'payments/payment.html', context)