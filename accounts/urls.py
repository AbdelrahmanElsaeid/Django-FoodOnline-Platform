from django.urls import path
from .views import registerUser, registerVendor, login, logout, custDashboard, myAccount, vendorDashboard, activate, forgetPassword, resest_password_validate,  resestPassword



urlpatterns = [
    path('registerUser/', registerUser , name="registerUser"),
    path('registerVendor/', registerVendor , name="registerVendor"),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('myAccount/', myAccount, name='myAccount'),
    path('custDashboard/', custDashboard, name='custDashboard'),
    path('vendorDashboard/', vendorDashboard, name='vendorDashboard'),
    
    path('activate/<uidb64>/<token>/', activate, name='activate'),

    path('forget-password/', forgetPassword, name='forget_password'),    
    path('reset-password-validate/<uidb64>/<token>/', resest_password_validate, name='reset_password_validate'),
    path('reset-password/', resestPassword, name='reset_password'),

  
]