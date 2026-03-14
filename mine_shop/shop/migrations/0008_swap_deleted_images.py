from django.db import migrations

def swap_deleted_images(apps, schema_editor):
    Product = apps.get_model('shop', 'Product')
    
    # These three specific images were completely deleted off Unsplash's CDN today. 
    # Swapping to brand new valid image IDs that exist.
    image_swaps = {
        "Jeans": "https://images.unsplash.com/photo-1541099649105-f69ad21f3246?auto=format&fit=crop&q=80&w=500",
        "Coffee Maker": "https://images.unsplash.com/photo-1520188740392-68b74ce126fc?auto=format&fit=crop&q=80&w=500",
        "Sci-Fi Novel": "https://images.unsplash.com/photo-1620336655174-32ff84dcc6bc?auto=format&fit=crop&q=80&w=500"
    }
    
    for name, img_url in image_swaps.items():
        Product.objects.filter(name=name).update(image_url=img_url)

class Migration(migrations.Migration):
    dependencies = [
        ('shop', '0007_restore_iphone_and_images'),
    ]

    operations = [
        migrations.RunPython(swap_deleted_images),
    ]
