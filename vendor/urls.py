from django.urls import path
from accounts.views import vendorDashboard
from .views import vprofile

urlpatterns = [

    path('', vendorDashboard, name='vendor' ),
    path('profile/', vprofile, name='vprofile')
]