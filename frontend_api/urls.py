from django.urls import path
from .views import *
urlpatterns = [
    path('register-api',RegisterView.as_view(),name='register_api'),
    path('login-api',LoginView.as_view(),name='login_api'),
    path('product-view-api',ProductViewApi.as_view(),name='product_view_api'),
    path('order-view-api',OrderListApi.as_view(),name='order_view_api'),
]