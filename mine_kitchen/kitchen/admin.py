from django.contrib import admin
from .models import FoodItem, CartItem, Order

admin.site.register(FoodItem)
admin.site.register(CartItem)
admin.site.register(Order)
