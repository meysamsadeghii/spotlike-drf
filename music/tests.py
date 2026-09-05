from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework.test import APIClient
from .models import Artist

User = get_user_model()

class AuthTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_register_and_login(self):
        res = self.client.post('/api/auth/register/', {'username':'u1','password':'pass'})
        self.assertEqual(res.status_code, 201)
        login = self.client.post('/api/auth/token/', {'username':'u1','password':'pass'})
        self.assertEqual(login.status_code, 200)

class APITests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user('test', password='pass')
        self.client.force_authenticate(self.user)

    def test_artist_str(self):
        a = Artist.objects.create(name='T')
        self.assertEqual(str(a), 'T')
