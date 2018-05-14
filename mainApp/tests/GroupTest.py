from django.test import TestCase
from rest_framework.test import APIRequestFactory, APIClient

from mainApp.models import User


class GroupTest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
                username='banifest', email='banifest@gmail.com', password='adminadmin')
        self.client = APIClient()
        self.client.force_login(user=self.user)

    def test_detail_group_create(self):
        response = self.client.post(
                '/api/users/banifest/groups/',
                {
                    'color': 'GREEN',
                    'priority': 2,
                    'name': 'test',
                }, format='json')
        self.assertEqual(response.status_code, 201)

    def test_detail_group_update_auth(self):
        response = self.client.post(
                '/api/users/banifest/groups/',
                {
                    'color': 'GREEN',
                    'priority': 2,
                    'name': 'test',
                }, format='json')
        response = self.client.patch(
                '/api/users/banifest/groups/{0}/'.format(response.data['id']),
                {
                    'name': 'NotTest',
                    'color': 'RED',
                    'priority': -1
                }, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'NotTest')
        self.assertEqual(response.data['color'], 'RED')
        self.assertEqual(response.data['priority'], -1)

    def test_detail_group_delete_auth(self):
        response = self.client.post(
                '/api/users/banifest/groups/',
                {
                    'color': 'GREEN',
                    'priority': 2,
                    'name': 'test',
                }, format='json')
        response = self.client.delete(
                '/api/users/banifest/groups/{0}/'.format(response.data['id']), format='json')
        self.assertEqual(response.status_code, 204)

    def test_list_group_with_auth(self):
        response = self.client.get('/api/users/banifest/groups/', format='json')
        self.assertEqual(response.status_code, 200)

    def test_list_group_without_auth(self):
        client = APIClient()
        response = client.get('/api/users/banifest/groups/', format='json')
        self.assertEqual(response.status_code, 403)
