import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mine_kitchen.settings')
django.setup()

from kitchen.models import FoodItem

# Clear existing if any (optional, let's just add new ones)
# FoodItem.objects.all().delete()

foods = [
    {"name": "Margherita Pizza", "description": "Classic cheese and tomato pizza.", "price": "12.99", "category": "Meals", "image_url": "https://images.unsplash.com/photo-1574071318508-1cdbab80d002?w=500&auto=format&fit=crop&q=60"},
    {"name": "Cheeseburger", "description": "Beef burger with cheese and fries.", "price": "10.49", "category": "Meals", "image_url": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?w=500&auto=format&fit=crop&q=60"},
    {"name": "Caesar Salad", "description": "Fresh lettuce with Caesar dressing.", "price": "8.99", "category": "Meals", "image_url": "https://images.unsplash.com/photo-1550304943-4f24f54ddde9?w=500&auto=format&fit=crop&q=60"},
    {"name": "Coca Cola", "description": "Chilled can of cola.", "price": "1.99", "category": "Drinks", "image_url": "https://images.unsplash.com/photo-1622483767028-3f66f32aef97?w=500&auto=format&fit=crop&q=60"},
    {"name": "Mango Smoothie", "description": "Fresh blended mango smoothie.", "price": "4.50", "category": "Drinks", "image_url": "https://images.unsplash.com/photo-1546250392-cd253fce85be?w=500&auto=format&fit=crop&q=60"},
    {"name": "Iced Coffee", "description": "Cold brewed coffee with milk.", "price": "3.50", "category": "Drinks", "image_url": "https://images.unsplash.com/photo-1461023058943-0708e5f23a54?w=500&auto=format&fit=crop&q=60"},
    {"name": "French Fries", "description": "Crispy golden french fries.", "price": "3.99", "category": "Snacks", "image_url": "https://images.unsplash.com/photo-1576107232684-1279f390859f?w=500&auto=format&fit=crop&q=60"},
    {"name": "Nachos", "description": "Tortilla chips with cheese and jalapenos.", "price": "6.99", "category": "Snacks", "image_url": "https://images.unsplash.com/photo-1513456811591-a1ed42d1f2b6?w=500&auto=format&fit=crop&q=60"},
    {"name": "Chocolate Chip Cookies", "description": "Warm baked cookies.", "price": "2.99", "category": "Desserts", "image_url": "https://images.unsplash.com/photo-1499636136210-6f4ee915583e?w=500&auto=format&fit=crop&q=60"},
]

for food_data in foods:
    food, created = FoodItem.objects.get_or_create(
        name=food_data['name'],
        defaults={
            'description': food_data['description'],
            'price': food_data['price'],
            'category': food_data['category'],
            'image_url': food_data['image_url'],
        }
    )
    if not created:
        food.category = food_data['category']
        food.save()

print("Kitchen database seeded successfully with categories!")
