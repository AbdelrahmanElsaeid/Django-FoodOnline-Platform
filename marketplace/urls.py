from django.urls import path, include
from .views import marketplace, marketplace_detail, add_to_cart, decrease_cart


urlpatterns = [
    path('',marketplace, name='marketplace'),
    path('<slug:vendor_slug>/',marketplace_detail, name='marketplace_detail'),
    path('add_to_cart/<int:food_id>/', add_to_cart, name='add_to_cart'),
    path('decrease_cart/<int:food_id>/', decrease_cart, name='decrease_cart'),


  
]