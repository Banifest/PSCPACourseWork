from django.contrib.auth.models import User
from rest_framework import serializers

from mainApp.models import Group, Reference


class UserSerializer(serializers.HyperlinkedModelSerializer):
    # references = serializers.HyperlinkedRelatedField(
    #         view_name='reference-detail',
    #         many=True,
    #         read_only=True,
    # )

    class Meta:
        model = User
        fields = ('url', 'username', 'first_name', 'last_name', 'email', 'references')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name', 'priority', 'color',)



class ReferenceSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Reference
        fields = ('id', 'url', 'name', 'user', 'group')
        extra_kwargs = {
            'group': {'view_name': 'group-detail'},
        }