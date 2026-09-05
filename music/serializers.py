from rest_framework import serializers
from .models import Artist, Album, Track, Playlist, PlaylistTrack, PlayEvent, Favorite
from django.contrib.auth import get_user_model

User = get_user_model()

class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = '__all__'

class AlbumSerializer(serializers.ModelSerializer):
    tracks = TrackSerializer(many=True, read_only=True)
    class Meta:
        model = Album
        fields = '__all__'

class ArtistSerializer(serializers.ModelSerializer):
    albums = AlbumSerializer(many=True, read_only=True)
    class Meta:
        model = Artist
        fields = '__all__'

class PlaylistTrackSerializer(serializers.ModelSerializer):
    track = TrackSerializer(read_only=True)
    class Meta:
        model = PlaylistTrack
        fields = ['id','track','order','added_at']

class PlaylistSerializer(serializers.ModelSerializer):
    playlist_tracks = PlaylistTrackSerializer(many=True, read_only=True)
    class Meta:
        model = Playlist
        fields = ['id','owner','title','description','is_public','created_at','playlist_tracks']
        read_only_fields = ['owner']

class PlayEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlayEvent
        fields = '__all__'

class FavoriteSerializer(serializers.ModelSerializer):
    track = TrackSerializer(read_only=True)
    class Meta:
        model = Favorite
        fields = ['id','track','added_at']
