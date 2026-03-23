from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import FoodItemViewSet, CartItemViewSet, OrderViewSet, CheckoutView, PartnerOrderItemViewSet
from . import views

router = DefaultRouter()
router.register(r'foods', FoodItemViewSet)
router.register(r'cart', CartItemViewSet, basename='cart')
router.register(r'orders', OrderViewSet, basename='orders')
router.register(r'partner/orders', PartnerOrderItemViewSet, basename='partner_orders')

urlpatterns = [
    path('', include(router.urls)),
    path('food/<int:food_id>/', views.kitchen_food_detail, name='kitchen_food_detail'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('checkout-success/', views.kitchen_checkout_success, name='kitchen_checkout_success'),
    path('payment/', views.kitchen_payment, name='kitchen_payment'),
]
