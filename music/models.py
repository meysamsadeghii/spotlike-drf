from django.db import models
from django.conf import settings

class Artist(models.Model):
    name = models.CharField(max_length=255)
    bio = models.TextField(blank=True)
    image = models.URLField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class Album(models.Model):
    artist = models.ForeignKey(Artist, related_name='albums', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    release_date = models.DateField(null=True, blank=True)
    cover = models.URLField(blank=True)

    def __str__(self):
        return f"{self.title} - {self.artist.name}"

class Track(models.Model):
    album = models.ForeignKey(Album, related_name='tracks', on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=255)
    duration = models.PositiveIntegerField(null=True, blank=True, help_text='duration in seconds')
    audio_url = models.URLField(blank=True)
    explicit = models.BooleanField(default=False)
    track_number = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.title

class Playlist(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='playlists', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.owner})"

class PlaylistTrack(models.Model):
    playlist = models.ForeignKey(Playlist, related_name='playlist_tracks', on_delete=models.CASCADE)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order']
        unique_together = ('playlist', 'track')

class PlayEvent(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    position = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.user} played {self.track} at {self.timestamp}"

class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='favorites', on_delete=models.CASCADE)
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'track')
