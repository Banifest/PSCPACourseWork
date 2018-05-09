from django.contrib.auth.models import AnonymousUser
from django.test import TestCase, RequestFactory
from rest_framework import response

from mainApp.models import User


class UserTest(TestCase):
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
                username='test123', email='test123@test.com', password='12345t')

    def test_details(self):
        request = self.factory.get('/api/users/')

        request.user = self.user

        request.user = AnonymousUser()
        print(request)
        self.assertEqual(request, 200)