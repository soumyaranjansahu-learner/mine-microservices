"""
URL configuration for mine_shop project.

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
from django.urls import path, include
from shop.views import (
    shop_home, shop_cart, shop_orders, shop_product_detail,
    order_cancel, order_return, order_exchange, action_success
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('shop.urls')),
    path('', shop_home, name='shop_home'),
    path('cart/', shop_cart, name='shop_cart'),
    path('orders/', shop_orders, name='shop_orders'),
    path('product/<int:product_id>/', shop_product_detail),
    path('shop/product/<int:product_id>/', shop_product_detail),
    # Add prefixed endpoints because Main Gateway proxies them with the prefix intact
    path('shop/order/<int:order_id>/cancel/', order_cancel),
    path('shop/order/<int:order_id>/return/', order_return),
    path('shop/order/<int:order_id>/exchange/', order_exchange),
    path('shop/action-success/<str:action>/', action_success),
    # And non-prefixed just in case
    path('order/<int:order_id>/cancel/', order_cancel),
    path('order/<int:order_id>/return/', order_return),
    path('order/<int:order_id>/exchange/', order_exchange),
    path('action-success/<str:action>/', action_success),
]
