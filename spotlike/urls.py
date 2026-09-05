from django.contrib import admin
from django.urls import path, include
from music import urls as music_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(music_urls)),
]
