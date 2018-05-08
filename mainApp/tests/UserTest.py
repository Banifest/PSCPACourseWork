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
        # Create an instance of a GET request.
        request = self.factory.get('/customer/details')

        # Recall that middleware are not supported. You can simulate a
        # logged-in user by setting request.user manually.
        request.user = self.user

        # Or you can simulate an anonymous user by setting request.user to
        # an AnonymousUser instance.
        request.user = AnonymousUser()

        # Test my_view() as if it were deployed at /customer/details
        #response = my_view(request)
        # Use this syntax for class-based views.
        #response = MyView.as_view()(request)
        self.assertEqual(response, 200)