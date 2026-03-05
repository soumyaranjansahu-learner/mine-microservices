import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mine_shop.settings')
django.setup()

from shop.models import Product

names = set()
duplicates = []
for p in Product.objects.all().order_by('id'):
    if p.name in names:
        duplicates.append(p.id)
    else:
        names.add(p.name)

print("Shop duplicates to delete:", len(duplicates), duplicates)
Product.objects.filter(id__in=duplicates).delete()
