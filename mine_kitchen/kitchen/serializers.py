from rest_framework import serializers
from .models import FoodItem, CartItem, Order

class FoodItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = FoodItem
        fields = '__all__'

class CartItemSerializer(serializers.ModelSerializer):
    food_item = FoodItemSerializer(read_only=True)
    food_item_id = serializers.PrimaryKeyRelatedField(
        queryset=FoodItem.objects.all(), source='food_item', write_only=True
    )

    class Meta:
        model = CartItem
        fields = ['id', 'user_id', 'food_item', 'food_item_id', 'quantity']
        read_only_fields = ['user_id']

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = '__all__'
