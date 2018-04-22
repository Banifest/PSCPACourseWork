from django.shortcuts import get_object_or_404
from rest_framework import viewsets, renderers
from rest_framework.decorators import action
from rest_framework.response import Response

from mainApp.permissions import permissions
from mainApp.models import Reference, Group, User
from mainApp.serializers import ReferenceSerializer, UserSerializer, GroupSerializer


class GroupViewSet(viewsets.ModelViewSet):
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs['pk']
        users_pk = kwargs['users_pk']
        user = User.objects.get(username=users_pk)
        queryset = Group.objects.filter(pk=pk, user=user)
        instance = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        users_pk = kwargs['users_pk']
        user = User.objects.get(username=users_pk)
        queryset = Group.objects.filter(user=user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (
         permissions.IsAuthenticated,
    )

    @action(methods=['post'], detail=True, permission_classes=[permissions.IsAuthenticated])
    def set_password(self, request, pk=None):
        return Response('')
        pass

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs['username']
        queryset = User.objects.filter(username=pk)
        instance = get_object_or_404(queryset, username=pk)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ReferenceViewSet(viewsets.ModelViewSet):

    queryset = Reference.objects.all()
    serializer_class = ReferenceSerializer

    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    def retrieve(self, request, *args, **kwargs):
        pk = kwargs['pk']
        users_pk = kwargs['users_pk']
        user = User.objects.get(username=users_pk)
        queryset = Reference.objects.filter(pk=pk, user=user)
        instance = get_object_or_404(queryset, pk=pk)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def list(self, request, *args, **kwargs):
        users_pk = kwargs['users_pk']
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
