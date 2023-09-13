from django.urls import path
from .views import registerUser, registerVendor, login, logout, custDashboard, myAccount, vendorDashboard, activate



urlpatterns = [
    path('registerUser/', registerUser , name="registerUser"),
    path('registerVendor/', registerVendor , name="registerVendor"),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('myAccount/', myAccount, name='myAccount'),
    path('custDashboard/', custDashboard, name='custDashboard'),
    path('vendorDashboard/', vendorDashboard, name='vendorDashboard'),
    
    path('activate/<uidb64>/<token>/', activate, name='activate')

  
]