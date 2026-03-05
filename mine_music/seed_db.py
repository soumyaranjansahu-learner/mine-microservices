import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mine_music.settings')
django.setup()

from music.models import Song

songs = [
    {"title": "Bohemian Rhapsody", "artist": "Queen", "genre": "Rock", "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3"},
    {"title": "Shape of You", "artist": "Ed Sheeran", "genre": "Pop", "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3"},
    {"title": "Blinding Lights", "artist": "The Weeknd", "genre": "Pop", "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-3.mp3"},
    {"title": "Hotel California", "artist": "Eagles", "genre": "Rock", "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3"},
    {"title": "Lose Yourself", "artist": "Eminem", "genre": "Hip Hop", "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-5.mp3"},
    {"title": "God's Plan", "artist": "Drake", "genre": "Hip Hop", "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-6.mp3"},
    {"title": "Take Five", "artist": "Dave Brubeck", "genre": "Jazz", "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-7.mp3"},
    {"title": "So What", "artist": "Miles Davis", "genre": "Jazz", "url": "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-8.mp3"}
]

for s_data in songs:
    Song.objects.get_or_create(
        title=s_data['title'],
        artist=s_data['artist'],
        defaults={
            'genre': s_data['genre'],
            'audio_file_url': s_data['url']
        }
    )

print("Music database seeded successfully with genres!")
