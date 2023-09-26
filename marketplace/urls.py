from django.urls import path, include
from .views import marketplace, vendor_detail, add_to_cart, decrease_cart, delete_cart


urlpatterns = [
    path('',marketplace, name='marketplace'),
    # path('cart/', cart, name='cart'),
    path('<slug:vendor_slug>/',vendor_detail, name='vendor_detail'),
    path('add_to_cart/<int:food_id>/', add_to_cart, name='add_to_cart'),
    path('decrease_cart/<int:food_id>/', decrease_cart, name='decrease_cart'),
    path('delete_cart/<int:cart_id>/', delete_cart, name='delete_cart'),


  
]