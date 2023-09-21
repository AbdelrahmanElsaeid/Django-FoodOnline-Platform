from django.urls import path, include
from .views import marketplace, marketplace_detail


urlpatterns = [
    path('',marketplace, name='marketplace'),
    path('<slug:vendor_slug>/',marketplace_detail, name='marketplace_detail'),

  
]