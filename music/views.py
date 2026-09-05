from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Artist, Album, Track, Playlist, PlaylistTrack, PlayEvent, Favorite
from .serializers import ArtistSerializer, AlbumSerializer, TrackSerializer, PlaylistSerializer, PlaylistTrackSerializer, PlayEventSerializer, FavoriteSerializer
from django.db import models
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated

class ArtistViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']

class AlbumViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Album.objects.select_related('artist').all()
    serializer_class = AlbumSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title','artist__name']

class TrackViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Track.objects.select_related('album__artist').all()
    serializer_class = TrackSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['title','album__title','album__artist__name']

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def play(self, request, pk=None):
        track = self.get_object()
        PlayEvent.objects.create(user=request.user, track=track, position=request.data.get('position'))
        return Response({'status':'ok'}, status=status.HTTP_201_CREATED)

class PlaylistViewSet(viewsets.ModelViewSet):
    serializer_class = PlaylistSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Playlist.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['post'])
    def add_track(self, request, pk=None):
        playlist = self.get_object()
        track_id = request.data.get('track_id')
        track = Track.objects.get(pk=track_id)
        order = (playlist.playlist_tracks.aggregate(models.Max('order'))['order__max'] or 0) + 1
        pt, created = PlaylistTrack.objects.get_or_create(playlist=playlist, track=track, defaults={'order':order})
        return Response(PlaylistTrackSerializer(pt).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def remove_track(self, request, pk=None):
        playlist = self.get_object()
        pt_id = request.data.get('playlist_track_id')
        PlaylistTrack.objects.filter(id=pt_id, playlist=playlist).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class FavoriteViewSet(viewsets.ModelViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user).select_related('track')

    def perform_create(self, serializer):
        track_id = self.request.data.get('track_id')
        track = Track.objects.get(pk=track_id)
        serializer.save(user=self.request.user, track=track)

class PlayEventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PlayEvent.objects.select_related('track','user').all()
    serializer_class = PlayEventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PlayEvent.objects.filter(user=self.request.user)
