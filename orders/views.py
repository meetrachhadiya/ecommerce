from django.shortcuts import render, redirect
from orders.models import Order
from django.contrib.auth.decorators import login_required
from django.contrib import messages

# Create your views here.

def order_confirm(request):
    return render(request, 'orders/order_confirm.html')

@login_required(login_url='login')
def orders_page(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    context = {"orders" : orders}
    return render(request, 'orders/orders.html', context)
    
def order_detail(request, order_id):
    try:
        order = Order.objects.get(order_id = order_id)
        print(order)
    except Exception as e:
        messages.warning(request, "order not found")    
    context = {
        'order' : order
    }
    return render(request, "orders/order_details.html", context)

from orders.forms import OrderCancelForm, OrderEditForm

def cancel_order(request, order_id):
    order = Order.objects.get(pk=order_id)
    if request.method == 'POST':
        form = OrderCancelForm(request.POST)
        if form.is_valid():
            order.delete()
            return redirect('orders-page')
    else:
        form = OrderCancelForm()
    return render(request, 'orders/cancel_order.html', {'form': form, 'order': order})

def edit_order(request, order_id):
    order = Order.objects.get(pk=order_id)
    if request.method == 'POST':
        form = OrderEditForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('order_details', order_id=order_id)
    else:
        form = OrderEditForm(instance=order)
    return render(request, 'orders/edit_order.html', {'form': form, 'order': order})

from orders.models import OrderItems

def remove_order_item(request, order_id, item_uid):
    if request.method == 'GET':
        order_item = OrderItems.objects.get(uid=item_uid)
        print(order_item)
        order_item.delete()
        order = Order.objects.get(order_id = order_id)
        if order.order_items.all().count() == 0:
            order.delete()
            messages.warning(request, "Since no order item is there order is deleted")
            return redirect('orders-page')
        # return redirect('edit_order')
    return redirect('edit_order', order_id=order_id)
