from django.urls import path
from accounts.views import vendorDashboard
from .views import vprofile, menu_builder,fooditems_by_category, add_category, edit_category, delete_category, add_food, edit_food, delete_food,opening_hours, add_opening_hours, remove_opening_hours

urlpatterns = [

    path('', vendorDashboard, name='vendor' ),
    path('profile/', vprofile, name='vprofile'),
    path('menu-builder/', menu_builder,name='menu_builder'),
    path('menu-builder/category/<int:pk>/', fooditems_by_category, name='fooditems_by_category'),
    
    #category crud
    path('menu-bulider/category/add/',add_category, name='add_category'),
    path('menu-bulider/category/edit/<int:pk>/',edit_category, name='edit_category'),
    path('menu-bulider/category/delete/<int:pk>/',delete_category, name='delete_category'),
        
    #food crud
    path('menu-bulider/food/add/',add_food, name='add_food'),
    path('menu-bulider/food/edit/<int:pk>/',edit_food, name='edit_food'),
    path('menu-bulider/food/delete/<int:pk>/',delete_food, name='delete_food'),

    # Opening Hour CRUD
    path('opening-hours/', opening_hours, name='opening_hours'),
    path('opening-hours/add/', add_opening_hours, name='add_opening_hours'),
    path('opening-hours/remove/<int:pk>/', remove_opening_hours, name='remove_opening_hours'),
]