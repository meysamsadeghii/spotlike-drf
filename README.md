# spotlike-drf

Starter Django REST Framework project inspired by Spotify (MVP).

Features
- Artists, Albums, Tracks
- Playlists (create, add/remove tracks)
- Play events (track play history)
- Favorites (user library)
- JWT authentication via SimpleJWT
- Search and filtering with DRF

Quick start (Docker)
1. Copy .env.example to .env and set DJANGO_SECRET_KEY
2. docker compose up --build -d
3. docker compose exec web python manage.py migrate
4. docker compose exec web python manage.py createsuperuser
5. docker compose exec web python manage.py loaddata sample_data.json

Local (without Docker)
- Use virtualenv, install requirements.txt and run migrate/create superuser

License: MIT
