from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpRequest
from django.views.generic import TemplateView
from rest_framework import viewsets

from mainApp.models import Reference, Group
from mainApp.serializers import ReferenceSerializer, UserSerializer, GroupSerializer


class AuthView(TemplateView):
    template_name = 'auth.html'

    def post(self, request: HttpRequest) -> HttpResponse:
        user = authenticate(username=request.POST['login'], password=request.POST['password'])
        if user is not None:
            # the password verified for the user
            if user.is_active:
                login(request, user )
                return HttpResponse(content='User is valid, active and authenticated')
            else:
                return HttpResponse(content='The password is valid, but the account has been disabled!')
        else:
            # the authentication system was unable to verify the username and password
            return HttpResponse(content='This user is not exist')


class IndexView(TemplateView):
    template_name = 'index.html'


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ReferenceViewSet(viewsets.ReadOnlyModelViewSet):

    queryset = Reference.objects.all()
    serializer_class = ReferenceSerializer
