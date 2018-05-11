from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, RequestFactory
from django.urls import include, path
from rest_framework import response, status
from rest_framework.reverse import reverse
from rest_framework.test import APIRequestFactory, APITestCase, URLPatternsTestCase, APIClient

from mainApp.models import User, Group, Reference
from mainApp.views import UserViewSet


class ReferenceTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = APIRequestFactory()
        self.user = User.objects.create_user(
                username='banifest', email='banifest@gmail.com', password='adminadmin')
        self.group = Group.objects.create(color='GREEN', priority=1, name='test', user=self.user)
        self.ref = Reference.objects.create(name='GREEN', ref_url='http://123.com', group=self.group, user=self.user)
        self.client = APIClient()
        self.client.force_login(user=self.user)

    def test_detail_ref_create(self):
        response = self.client.post(
                '/api/users/banifest/references/',
                {
                    'name': 'test',
                    'ref_url': 'http://test.com',
                    'group': self.group.id
                }, format='json')
        self.assertEqual(response.status_code, 201)

    def test_detail_ref_update_auth(self):
        response = self.client.patch(
                '/api/users/banifest/references/{0}/'.format(self.ref.id),
                {
                    'name': 'NotTest',
                    'ref_url': 'http://Not-test.com',
                }, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data['name'], 'NotTest')
        self.assertEqual(response.data['ref_url'], 'http://Not-test.com')

    def test_detail_user_delete_auth(self):
        response = self.client.delete('/api/users/banifest/references/{0}/'.format(self.ref.id), format='json')
        self.assertEqual(response.status_code, 204)

    def test_list_ref_with_auth(self):
        response = self.client.get('/api/users/banifest/references/', format='json')
        self.assertEqual(response.status_code, 999)

    def test_detail_ref_with_auth(self):
        response = self.client.get('/api/users/banifest/references/', format='json')
        self.assertEqual(response.status_code, 200)

    def test_list_ref_without_auth(self):
        client = APIClient()
        response = client.get('/api/users/', format='json')
        self.assertEqual(response.status_code, 403)
