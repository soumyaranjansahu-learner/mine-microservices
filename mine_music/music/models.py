from django.db import models

class Song(models.Model):
    GENRE_CHOICES = [
        ('Pop', 'Pop'),
        ('Rock', 'Rock'),
        ('Hip Hop', 'Hip Hop'),
        ('Jazz', 'Jazz'),
        ('Classical', 'Classical'),
        ('Electronic', 'Electronic'),
        ('Country', 'Country'),
        ('Unknown', 'Unknown'),
    ]

    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    album = models.CharField(max_length=200, blank=True, null=True)
    genre = models.CharField(max_length=100, choices=GENRE_CHOICES, default='Unknown')
    audio_file_url = models.URLField(max_length=500) # Simulating an audio file URL
    cover_image_url = models.URLField(blank=True, null=True)
    play_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.artist}"

class Playlist(models.Model):
    user_id = models.IntegerField()
    name = models.CharField(max_length=200)
    songs = models.ManyToManyField(Song, related_name='playlists')

    def __str__(self):
        return f"{self.name} by User {self.user_id}"
