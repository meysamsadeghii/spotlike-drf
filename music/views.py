from rest_framework import viewsets, permissions, filters, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from .models import Artist, Album, Track, Playlist, PlaylistTrack, PlayEvent, Favorite
from .serializers import ArtistNestedSerializer as ArtistSerializer, AlbumNestedSerializer as AlbumSerializer, TrackSerializer, PlaylistSerializer, PlaylistTrackSerializer, PlayEventSerializer, FavoriteSerializer
from django.db import models
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework import serializers

User = get_user_model()

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

# Registration and profile endpoints
class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ('username','email','password')

    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['username'], email=validated_data.get('email'), password=validated_data['password'])
        return user

class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({'id': user.id, 'username': user.username}, status=status.HTTP_201_CREATED)

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','email','first_name','last_name')

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = ProfileSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = ProfileSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)
