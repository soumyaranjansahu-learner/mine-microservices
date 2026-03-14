import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mine_shop.settings')
django.setup()

from shop.models import Category, Product

categories_data = [
    {"name": "Electronics", "description": "Gadgets and tech"},
    {"name": "Clothing", "description": "Apparel and fashion"},
    {"name": "Home", "description": "Home furniture and appliances"},
    {"name": "Books", "description": "Novels and textbooks"}
]

cat_objects = {}
for data in categories_data:
    cat, _ = Category.objects.get_or_create(name=data['name'], defaults={'description': data['description']})
    cat_objects[data['name']] = cat

products = [
    {"name": "Laptop", "desc": "High performance", "price": "1299.99", "cat": "Electronics", "stock": 30, "img": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=800", "features": {"RAM": ["8GB", "16GB", "32GB"], "Color": ["Silver", "Space Gray"]}},
    {"name": "T-Shirt", "desc": "Cotton casual", "price": "19.99", "cat": "Clothing", "stock": 100, "img": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=800", "features": {"Size": ["S", "M", "L", "XL"], "Color": ["White", "Black", "Grey"]}},
    {"name": "Jeans", "desc": "Denim wear", "price": "49.99", "cat": "Clothing", "stock": 80, "img": "https://images.unsplash.com/photo-1542272604-78fe0840c3cb?w=800", "features": {"Size": ["28", "30", "32", "34"], "Color": ["Light Blue", "Dark Blue", "Black"]}},
    {"name": "Coffee Maker", "desc": "Brew fresh coffee", "price": "89.99", "cat": "Home", "stock": 20, "img": "https://images.unsplash.com/photo-1495474472205-16284eb4308c?w=800", "features": {"Color": ["Black", "Silver", "Red"]}},
    {"name": "Desk Lamp", "desc": "LED lamp", "price": "29.99", "cat": "Home", "stock": 40, "img": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=800", "features": {"Lighting": ["Warm", "Cool", "Neutral"]}},
    {"name": "Sci-Fi Novel", "desc": "Space adventure", "price": "14.99", "cat": "Books", "stock": 60, "img": "https://images.unsplash.com/photo-1614729939124-032f0b5609ce?w=800", "features": {"Format": ["Paperback", "Hardcover", "Audiobook"]}}
]

for p_data in products:
    p, created = Product.objects.get_or_create(
        name=p_data['name'],
        category=cat_objects[p_data['cat']],
        defaults={
            'description': p_data['desc'],
            'price': p_data['price'],
            'stock': p_data['stock'],
            'image_url': p_data['img'],
            'features': p_data.get('features', {})
        }
    )
    if not created:
        p.features = p_data.get('features', {})
        p.save()

print("Shop database seeded successfully with categories and products!")
