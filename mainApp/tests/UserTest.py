from django.contrib.auth.models import AnonymousUser
from django.test import TestCase
from rest_framework.test import APIRequestFactory, APIClient

from mainApp.models import User
from mainApp.views import UserViewSet


class UserTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
                username='banifest', email='banifest@gmail.com', password='adminadmin')

    def test_list_user_with_auth(self):
        client = APIClient()
        client.login(username='banifest', password='adminadmin')
        response = client.get('/api/users/', format='json')
        self.assertEqual(response.status_code, 200)

    def test_list_user_without_auth(self):
        client = APIClient()
        response = client.get('/api/users/', format='json')
        self.assertEqual(response.status_code, 403)

    def test_detail_user_with_auth(self):
        client = APIClient()
        client.login(username='banifest', password='adminadmin')
        response = client.get('/api/users/banifest/', format='json')
        self.assertEqual(response.status_code, 200)

    def test_detail_user_without_auth(self):
        request = self.factory.get('/api/users/banifest/', format='json')
        request.user = AnonymousUser()
        response = UserViewSet.as_view({'get': 'detail'})(request)
        self.assertEqual(response.status_code, 403)

    def test_detail_user_create(self):
        client = APIClient()
        response = client.post('/api/users/', {'username': 'test', 'password': '123'}, format='json')
        self.assertEqual(response.status_code, 201)

    def test_detail_user_update_auth(self):
        client = APIClient()
        client.login(username='banifest', password='adminadmin')
        response = client.patch('/api/users/banifest/', {'first_name': 'test', 'last_name': 'test'}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['first_name'], 'test')
        self.assertEqual(response.data['last_name'], 'test')

    def test_detail_user_delete_auth(self):
        client = APIClient()
        response = client.post('/api/users/', {'username': 'test', 'password': '123'}, format='json')
        client.login(username='test', password='123')
        response = client.delete('/api/users/test/', format='json')
        self.assertEqual(response.status_code, 204)
