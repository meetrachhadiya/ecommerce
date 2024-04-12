from django.urls import path
from products.views import (
    get_product,
)

urlpatterns = [
    path('<uid>/', get_product, name='get-product'),
]