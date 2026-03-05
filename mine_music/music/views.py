from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Song, Playlist
from .serializers import SongSerializer, PlaylistSerializer

class SongViewSet(viewsets.ModelViewSet):
    queryset = Song.objects.all()
    serializer_class = SongSerializer

    def get_queryset(self):
        queryset = Song.objects.all()
        genre = self.request.query_params.get('genre', None)
        search = self.request.query_params.get('search', None)
        
        if genre and genre != 'All':
            queryset = queryset.filter(genre=genre)
        if search:
            queryset = queryset.filter(title__icontains=search) | queryset.filter(artist__icontains=search)
            
        return queryset

    @action(detail=False, methods=['get'])
    def genres(self, request):
        genres = Song.objects.values_list('genre', flat=True).distinct()
        return Response([g for g in genres if g])

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [AllowAny]
        else:
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    @action(detail=True, methods=['post'], permission_classes=[AllowAny])
    def stream(self, request, pk=None):
        song = self.get_object()
        song.play_count += 1
        song.save()
        return Response({'message': 'Streaming URL ready', 'audio_file_url': song.audio_file_url, 'play_count': song.play_count})

class PlaylistViewSet(viewsets.ModelViewSet):
    serializer_class = PlaylistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Playlist.objects.filter(user_id=self.request.user.id)

    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user.id)

# --- UI Views ---
from django.shortcuts import render

def music_home(request):
    return render(request, 'music.html')
