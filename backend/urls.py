from django.urls import path
from .views import *
urlpatterns = [
    path('',backend_index,name='backend_index'),
    path('signin',signin,name='signin'),
    path('signout',signout,name='signout'),
    
    #Customer
    path('customer',customer,name='customer'),
    path('edit-customer/<int:pk>',edit_customer,name='edit_customer'),
    path('delete-customer/<int:pk>',delete_customer,name='delete_customer'),
    
    #Product
    path('product',product,name='product'),
    path('create-product',create_product,name='create_product'),
    path('edit-product/<int:pk>',edit_product,name='edit_product'),
    path('delete-product/<int:pk>',delete_product,name='delete_product'),
    
    
    #Orders
    path('order-view',order_view,name="order_view"),
    path('order-view-detail/<str:order_id>',order_view_detail,name="order_view_detail"),
    path('update-order-status/', update_order_status, name='update_order_status'),
]
