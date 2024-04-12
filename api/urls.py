from django.urls import path, include
from api.views import products, login, ProductViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='products')

urlpatterns = [
    # path('products/', products, name='products'),
    path('login/', login, name='login'),
    path('', include(router.urls)),
]

