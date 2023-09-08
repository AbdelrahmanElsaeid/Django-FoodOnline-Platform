from django.urls import path
from .views import registerUser, registerVendor



urlpatterns = [
    path('registerUser', registerUser , name="registerUser"),
    path('registerVendor', registerVendor , name="registerVendor"),

  
]