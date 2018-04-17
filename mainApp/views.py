from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpRequest
from django.views.generic import TemplateView
from rest_framework import viewsets, renderers
from rest_framework.decorators import detail_route, action
from rest_framework.response import Response
from rest_framework.utils import json

from mainApp.permissions import permissions, IsOwnerOrReadOnly
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


class RegView(TemplateView):
    template_name = 'reg.html'


class MainView(TemplateView):
    template_name = 'main.html'


class GroupViewSet(viewsets.ModelViewSet):
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    )

    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def references(self, request, pk=None):
        user = self.get_object()
        references = Reference.objects.filter(user=user).all()

        return Response(user)



class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (
         permissions.IsAuthenticatedOrReadOnly,
         IsOwnerOrReadOnly, )


    # @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    # def references(self, request, pk=None):
    #     user = self.get_object()
    #     references = Reference.objects.filter(user=user).all()
    #
    #     return Response(json.dumps([reference for reference in references]))


class ReferenceViewSet(viewsets.ModelViewSet):

    queryset = Reference.objects.all()
    serializer_class = ReferenceSerializer

    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user,
                            group=Group.objects.get(id=self.request.data['group']))
        except:
            serializer.save(user=self.request.user,
                            group=Group.objects.first())
