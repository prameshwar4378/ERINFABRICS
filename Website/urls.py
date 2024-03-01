"""
URL configuration for ERINFABRICS project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from Website.views import *
urlpatterns = [
    path('', index, name='index'),
    path('test', test, name='test'),
    path('product_details/<int:id>', product_details,name="product_details"),
    path('add-to-cart/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart, name='cart'),
    path('update_cart_item/', update_cart_item, name='update_cart_item'),
    path('delete_item_from_cart/<int:id>', delete_item_from_cart, name='delete_item_from_cart'),
    path('update_profile_from_checkout/', update_profile_from_checkout, name='update_profile_from_checkout'),
    path('checkout/', checkout, name='checkout'),
    path('create_order/', create_order, name='create_order'),
    path('order_success/', order_success, name='order_success'),
] 
