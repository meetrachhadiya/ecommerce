from django.urls import path
from carts.views import (
    add_to_cart,
    cart,
    remove_from_cart,
    remove_coupon,
    update_quantity,
    checkout,
    continue_to_payment,
    payment,
    buy_now
)

urlpatterns = [
    path('', cart, name='cart'), 
    path('remove/<uid>', remove_from_cart, name='remove_from_cart'), 
    path('remove-coupon/<uid>', remove_coupon, name='remove_coupon'), 
    path('add-to-cart/<uid>', add_to_cart, name='add-to-cart'), 
    path('buy-now/<uid>', buy_now, name='buy-now'), 
    path('update-quantity/', update_quantity, name='update-quantity'), 
    path('checkout/', checkout, name='checkout'),
    path('continue-to-payment/', continue_to_payment, name='continue-to-payment'),
    path('payment/', payment, name='payment'),
] 