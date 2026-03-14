from django.db import migrations

def restore_iphone_and_images(apps, schema_editor):
    Product = apps.get_model('shop', 'Product')
    Category = apps.get_model('shop', 'Category')
    
    # 1. Restore iPhone 17 Pro Max
    electronics_cat, _ = Category.objects.get_or_create(name='Electronics')
    Product.objects.get_or_create(
        name="iphone 17 pro max",
        defaults={
            'category': electronics_cat,
            'description': 'The ultimate smartphone experience. Featuring the A18 Pro chip, a stunning 6.9-inch Super Retina XDR display with ProMotion, and a revolutionary 48MP triple-camera system capable of spatial video recording. Engineered with aerospace-grade titanium for maximum durability and thermal efficiency. Includes advanced AI capabilities and all-day battery life.',
            'price': 699.99,
            'stock': 49,
            'image_url': 'https://images.unsplash.com/photo-1695048133142-1a20484d2569?auto=format&fit=crop&q=80&w=500',
            'features': {'Color': ['Titanium', 'Black', 'White', 'Natural'], 'Storage': ['256GB', '512GB', '1TB']}
        }
    )
    
    # 2. Fix Broken Images for existing products
    image_fixes = {
        "Laptop": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?auto=format&fit=crop&q=80&w=500",
        "T-Shirt": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?auto=format&fit=crop&q=80&w=500",
        "Jeans": "https://images.unsplash.com/photo-1542272604-78fe0840c3cb?auto=format&fit=crop&q=80&w=500",
        "Coffee Maker": "https://images.unsplash.com/photo-1495474472205-16284eb4308c?auto=format&fit=crop&q=80&w=500",
        "Desk Lamp": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?auto=format&fit=crop&q=80&w=500",
        "Sci-Fi Novel": "https://images.unsplash.com/photo-1614729939124-032f0b5609ce?auto=format&fit=crop&q=80&w=500"
    }
    
    for name, img_url in image_fixes.items():
        Product.objects.filter(name=name).update(image_url=img_url)

class Migration(migrations.Migration):
    dependencies = [
        ('shop', '0006_remove_smartphone_and_duplicates'),
    ]

    operations = [
        migrations.RunPython(restore_iphone_and_images),
    ]
