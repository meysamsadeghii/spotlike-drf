from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Artist

User = get_user_model()

class BasicTests(TestCase):
    def test_artist_str(self):
        a = Artist.objects.create(name='T')
        self.assertEqual(str(a), 'T')
