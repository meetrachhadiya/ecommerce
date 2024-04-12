from django import forms
from .models import Order

class OrderCancelForm(forms.Form):
    confirm_cancel = forms.BooleanField(label='Confirm Cancel', required=True)

class OrderEditForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['address', 'order_total']  # Add more fields as needed for editing orders
