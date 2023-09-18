from django.urls import path
from accounts.views import vendorDashboard
from .views import vprofile, menu_builder,fooditems_by_category, add_category

urlpatterns = [

    path('', vendorDashboard, name='vendor' ),
    path('profile/', vprofile, name='vprofile'),
    path('menu-builder/', menu_builder,name='menu_builder'),
    path('menu-builder/category/<int:pk>/', fooditems_by_category, name='fooditems_by_category'),
    
    #category crud
    path('menu-bulider/category/add/',add_category, name='add_category')
]