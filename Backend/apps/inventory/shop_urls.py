from django.urls import path
from .shop_views import ShopListView, ShopCartView

app_name = "shop"
urlpatterns = [
    path("",      ShopListView.as_view(), name="list"),
    path("cart/", ShopCartView.as_view(), name="cart"),
]
