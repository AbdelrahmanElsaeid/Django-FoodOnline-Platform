from django.urls import path
from accounts.views import custDashboard
from .views import cprofile, my_orders, order_detail
urlpatterns = [

    path('', custDashboard, name='customer' ),
    path('profile/', cprofile, name='cprofile'),
    path('my_orders/', my_orders, name='customer_my_orders'),
    path('order_detail/<int:order_number>/', order_detail, name='order_detail'),


]