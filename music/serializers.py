from rest_framework import serializers
from .models import Artist, Album, Track, Playlist, PlaylistTrack, PlayEvent, Favorite
from django.contrib.auth import get_user_model

User = get_user_model()

class ArtistNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Artist
        fields = ['id','name','image']

class AlbumNestedSerializer(serializers.ModelSerializer):
    artist = ArtistNestedSerializer(read_only=True)
    class Meta:
        model = Album
        fields = ['id','title','artist','cover']

class TrackSerializer(serializers.ModelSerializer):
    album = AlbumNestedSerializer(read_only=True)
    class Meta:
        model = Track
        fields = ['id','title','duration','audio_url','explicit','track_number','album']

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
    track = TrackSerializer(read_only=True)
    class Meta:
        model = PlayEvent
        fields = ['id','track','timestamp','position']

class FavoriteSerializer(serializers.ModelSerializer):
    track = TrackSerializer(read_only=True)
    class Meta:
        model = Favorite
        fields = ['id','track','added_at']
