from rest_framework import serializers
from .models import FoodItem, CartItem, Order, OrderItem

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

class OrderItemSerializer(serializers.ModelSerializer):
    food_item = FoodItemSerializer(read_only=True)
    user_id = serializers.IntegerField(source='order.user_id', read_only=True)
    shipping_address = serializers.CharField(source='order.shipping_address', read_only=True)
    contact_number = serializers.CharField(source='order.contact_number', read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'food_item', 'quantity', 'price', 'user_id', 'shipping_address', 'contact_number']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
