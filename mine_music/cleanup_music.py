import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mine_music.settings')
django.setup()

from music.models import Song

names = set()
duplicates = []
for p in Song.objects.all().order_by('id'):
    if p.title in names:
        duplicates.append(p.id)
    else:
        names.add(p.title)

print("Music duplicates to delete:", len(duplicates), duplicates)
Song.objects.filter(id__in=duplicates).delete()
