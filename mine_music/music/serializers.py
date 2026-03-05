from rest_framework import serializers
from .models import Song, Playlist

class SongSerializer(serializers.ModelSerializer):
    class Meta:
        model = Song
        fields = '__all__'

class PlaylistSerializer(serializers.ModelSerializer):
    songs_details = SongSerializer(source='songs', many=True, read_only=True)
    song_ids = serializers.PrimaryKeyRelatedField(
        queryset=Song.objects.all(), source='songs', many=True, write_only=True
    )

    class Meta:
        model = Playlist
        fields = ['id', 'user_id', 'name', 'songs_details', 'song_ids']
        read_only_fields = ['user_id']
