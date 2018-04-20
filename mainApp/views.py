from rest_framework import viewsets, renderers
from rest_framework.decorators import detail_route, action
from rest_framework.response import Response

from mainApp.permissions import permissions, IsOwnerOrReadOnly
from mainApp.models import Reference, Group, User
from mainApp.serializers import ReferenceSerializer, UserSerializer, GroupSerializer


class GroupViewSet(viewsets.ModelViewSet):
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
    )

    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (
         permissions.IsAuthenticatedOrReadOnly,
    )

    @action(detail=True, renderer_classes=[renderers.StaticHTMLRenderer])
    def refs(self, request, pk=None):

        return Response()


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
