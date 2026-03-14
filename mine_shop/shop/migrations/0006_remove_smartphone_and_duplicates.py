# Generated manually to purge duplicates and the Smartphone product on Render

from django.db import migrations
from django.db.models import Min

def remove_smartphone_and_dupes(apps, schema_editor):
    Product = apps.get_model('shop', 'Product')
    
    # Remove smartphone product
    Product.objects.filter(name__icontains="Smartphone").delete()
    
    # Remove all duplicate products (keep the oldest one per name)
    names = Product.objects.values_list('name', flat=True).distinct()
    for name in names:
        if name:
            first_id = Product.objects.filter(name=name).aggregate(Min('id'))['id__min']
            Product.objects.filter(name=name).exclude(id=first_id).delete()

class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0005_cartitem_selected_features_order_action_reason_and_more'),
    ]

    operations = [
        migrations.RunPython(remove_smartphone_and_dupes),
    ]
