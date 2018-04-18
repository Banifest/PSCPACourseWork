from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpRequest
from django.shortcuts import redirect
from django.views.generic import TemplateView
from rest_framework import viewsets, renderers
from rest_framework.decorators import detail_route, action
from rest_framework.response import Response
from rest_framework.utils import json

from mainApp.permissions import permissions, IsOwnerOrReadOnly
from mainApp.models import Reference, Group
from mainApp.serializers import ReferenceSerializer, UserSerializer, GroupSerializer

class GroupViewSet(viewsets.ModelViewSet):
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        IsOwnerOrReadOnly,
    )

    queryset = Group.objects.all()
    serializer_class = GroupSerializer



class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (
         permissions.IsAuthenticatedOrReadOnly,
         IsOwnerOrReadOnly, )

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
