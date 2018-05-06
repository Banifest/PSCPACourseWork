from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.utils import json

from mainApp.permissions import permissions, IsUserOwner, IsOwnerObj
from mainApp.models import Reference, Group, User
from mainApp.serializers import ReferenceSerializer, UserSerializer, GroupSerializer


class GroupViewSet(viewsets.ModelViewSet):
    permission_classes = (
        IsOwnerObj,
        permissions.IsAuthenticated,
    )

    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs['pk']
        users_pk = kwargs['users_username']
        user = User.objects.get(username=users_pk)
        queryset = Group.objects.filter(pk=pk, user=user)
        instance = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        users_pk = kwargs['users_username']
        user = User.objects.get(username=users_pk)
        queryset = Group.objects.filter(user=user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(
                user=self.request.user
        )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (
        permissions.IsAuthenticated,
        IsUserOwner,
    )

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs['username']
        queryset = User.objects.filter(username=pk)
        instance = get_object_or_404(queryset, username=pk)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save()
        user = User.objects.filter(username=self.request.data['username']).first()
        user.set_password('123')
        user.save()


@csrf_exempt
def user_login(request):
    request.data = json.loads(request.body)
    user = authenticate(username=request.data['username'], password=request.data['password'])
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponse(
                    content=json.dumps({'status': 'success'}),
                    status=201,
                    content_type='application/json'
            )
        else:
            return HttpResponse(
                    json.dumps({'status': "don't right login or password"}),
                    status=401,
                    content_type='application/json'
            )
    else:
        return HttpResponse(
                json.dumps({'status': "don't right login or password"}),
                status=401,
                content_type='application/json'
        )


class ReferenceViewSet(viewsets.ModelViewSet):
    queryset = Reference.objects.all()
    serializer_class = ReferenceSerializer

    permission_classes = (
        IsOwnerObj,
        permissions.IsAuthenticated,
    )

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs['pk']
        users_pk = kwargs['users_username']
        user = User.objects.get(username=users_pk)
        queryset = Reference.objects.filter(pk=pk, user=user)
        instance = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        users_pk = kwargs['users_username']
        user = User.objects.get(username=users_pk)
        queryset = Reference.objects.filter(user=user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user,
                            group=Group.objects.get(id=self.request.data['group']))
        except:
            serializer.save(user=self.request.user,
                            group=Group.objects.first())
