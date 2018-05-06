import json

from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import permissions, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from mainApp.models import Group
from mainApp.permissions import IsOwnerObj, IsUserOwner
from mainApp.serializers import GroupSerializer, UserSerializer
from mainApp.models import User

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
