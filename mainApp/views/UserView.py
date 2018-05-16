import json

from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpRequest
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from mainApp.models import User
from mainApp.permissions import IsUserOwner
from mainApp.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    permission_classes = (
        permissions.IsAuthenticated,
        IsUserOwner,
    )

    def get_permissions(self):
        if self.action == 'create':
            permission_classes = [permissions.AllowAny]
        elif self.action == 'login':
            permission_classes = [permissions.AllowAny]
        else:
            permission_classes = [
                IsUserOwner,
                permissions.IsAuthenticated,
            ]
        return [permission() for permission in permission_classes]

    @action(methods=['POST'], detail=True, url_path='login')
    def login(self, request: HttpRequest, username=None):
        user = authenticate(username=username, password=request.data['password'])
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
                        json.dumps({'detail': "don't right login or password"}),
                        status=401,
                        content_type='application/json'
                )
        else:
            return HttpResponse(
                    json.dumps({'detail': "don't right login or password"}),
                    status=401,
                    content_type='application/json'
            )

    @action(methods=['PATCH'], detail=True, url_path='change-password')
    def change_password(self, request: HttpRequest, username=None):
        user = User.objects.filter(username=username).first()
        if user == request.user:
            user.set_password(self.request.data['password'])
            user.save()
            return Response('{"detail": "password change successful"}')
        else:
            res = Response('{"detail": "bad request"}')
            res.status_code = 400
            return res

    # @etag()
    # @cache_response(key_func=)
    def retrieve(self, request, *args, **kwargs):
        pk = kwargs['username']
        queryset = User.objects.filter(username=pk)
        instance = get_object_or_404(queryset, username=pk)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_create(self, serializer):
        if 'password' not in self.request.data or self.request.data['password'] == '':
            res = Response('{"detail": "password is empty"}')
        serializer.save()
        user = User.objects.filter(username=self.request.data['username']).first()
        user.set_password(self.request.data['password'])
        user.save()
