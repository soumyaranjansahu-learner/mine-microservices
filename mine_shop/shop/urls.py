from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, ProductViewSet, CartItemViewSet, OrderViewSet, CheckoutView
from . import views

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'products', ProductViewSet)
router.register(r'cart', CartItemViewSet, basename='cart')
router.register(r'orders', OrderViewSet, basename='orders')

urlpatterns = [
    path('', include(router.urls)),
    path('product/<int:product_id>/', views.shop_product_detail, name='shop_product_detail'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('checkout-success/', views.shop_checkout_success, name='shop_checkout_success'),
    path('payment/', views.shop_payment, name='shop_payment'),
    path('order/<int:order_id>/cancel/', views.order_cancel, name='order_cancel'),
    path('order/<int:order_id>/return/', views.order_return, name='order_return'),
    path('order/<int:order_id>/exchange/', views.order_exchange, name='order_exchange'),
    path('action-success/<str:action>/', views.action_success, name='action_success'),
]
