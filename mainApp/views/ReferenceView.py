from rest_framework import permissions, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response

from mainApp.models import Group, Reference
from mainApp.models import User
from mainApp.permissions import IsOwnerObj
from mainApp.serializers import ReferenceSerializer


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
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        else:
            serializer = self.get_serializer(queryset, many=True)
            return Response(serializer.data)

    def perform_create(self, serializer):
        try:
            serializer.save(user=self.request.user,
                            group=Group.objects.get(id=self.request.data['group']))
        except:
            serializer.save(user=self.request.user,
                            group=Group.objects.first())
