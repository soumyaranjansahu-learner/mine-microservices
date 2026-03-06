from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SongViewSet, PlaylistViewSet

router = DefaultRouter()
router.register(r'songs', SongViewSet)
router.register(r'playlists', PlaylistViewSet, basename='playlists')

urlpatterns = [
    path('', include(router.urls)),
    path('song/<int:song_id>/', views.music_song_detail, name='music_song_detail'),
]
