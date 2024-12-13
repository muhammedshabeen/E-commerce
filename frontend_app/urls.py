from django.urls import path
from .views import *
urlpatterns = [
    path('frontend-login',frontend_login,name="frontend_login"),
    path('frontend-register',frontend_register,name="frontend_register"),
    path('frontend-logout',frontend_logout,name="frontend_logout"),
    path('',home,name='home'),
    path('product-detail/<slug:slug>',product_detail,name='product_detail'),
    path('add-to-cart',add_to_cart,name='add_to_cart'),
    path('add-to-cart-home',add_to_cart_home,name='add_to_cart_home'),
    path('view-cart',view_cart,name='view_cart'),
    path('update-cart',update_cart, name='update_cart'),
    path('delete-cart-item/<int:pk>',delete_cart_item, name='delete_cart_item'),
    path('add_address',add_address, name='add_address'),
    path('update_address',update_address, name='update_address'),
    path('checkout',checkout, name='checkout'),
    path('order-confirmation/<str:order_id>',order_confirmation, name='order_confirmation'),
    path('orders', user_orders, name='user_orders'),
    path('add-review/<int:product_id>',add_review, name='add_review'),
]
