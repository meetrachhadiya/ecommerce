from django.urls import path
from orders.views import (
    order_confirm,
    order_detail,
    cancel_order,
    edit_order,
    remove_order_item
)

urlpatterns = [
    path('confirm', order_confirm, name='order-confirm'),
    path('<order_id>/', order_detail, name='get-order'),
    path('<order_id>/cancel/', cancel_order, name='cancel_order'),
    path('<order_id>/edit/', edit_order, name='edit_order'),
    path('<order_id>/edit/remove/<item_uid>', remove_order_item, name='remove-order-item'),
]