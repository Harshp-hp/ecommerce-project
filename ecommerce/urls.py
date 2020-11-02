
from django.contrib import admin
from django.urls import path
from .views import Index, Signup, Login, logout, Checkout, OrderView
from .views import Cart
from .middlewares.auth import auth_middleware

urlpatterns = [
    path('', Index.as_view(), name='homepage'),
    path('signup', Signup.as_view(), name='signup'),
    path('login', Login.as_view(), name='login'),
    path('logout', logout,name='logout'),
    path('cart', Cart.as_view(),name='cart'),
    path('checkout', Checkout.as_view(),name='checkout'),
    path('order', auth_middleware(OrderView.as_view()), name='order'),
]
