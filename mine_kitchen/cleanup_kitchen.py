import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mine_kitchen.settings')
django.setup()

from kitchen.models import FoodItem

names = set()
duplicates = []
for p in FoodItem.objects.all().order_by('id'):
    if p.name in names:
        duplicates.append(p.id)
    else:
        names.add(p.name)

print("Kitchen duplicates to delete:", len(duplicates), duplicates)
FoodItem.objects.filter(id__in=duplicates).delete()
