from django.urls import path
from accounts.views import (
    loginUser,
    registerUser,
    activateUser,
    logoutUser,
    reset_password,
    reset_password_confirm,
    change_password,
    user_profile,
    address,
)
from orders.views import orders_page

urlpatterns = [
    path('user/<str:email>/', user_profile, name='profile'),
    path('login/', loginUser, name="login"),
    path('register/', registerUser, name="register"),
    path('activate/<str:email_token>/', activateUser, name="activate"),
    path('password/reset/', reset_password, name="reset-password"),
    path('password/reset/<str:reset_password_token>/', reset_password_confirm, name="reset-password-confirm"),
    path('password/change/', change_password, name="change-password"),
    path('logout/', logoutUser, name="logout"),
    path('address/', address, name="address"),
    path('orders/', orders_page, name="orders-page"),
]