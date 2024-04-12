from django.urls import path
from home.views import (
    index,
    search,
    temp,
)

urlpatterns = [
    path('', index, name="home"),
    path('search/', search, name="search"),
    path('temp/', temp)
]