from rest_framework import serializers
from rest_framework.relations import HyperlinkedIdentityField

from mainApp.models import Group, Reference, User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
            view_name='user-detail',
            lookup_field='username'
    )
    class Meta:
        model = User
        fields = ('url',
                  'username',
                  'first_name',
                  'last_name',
                  'email',
                  #'url',
                  #'refs',
                  'groups',
                  )


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = (
            'id',
            'name',
            'priority',
            'color',
            'user'
        )


class ReferenceSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(
            view_name='user-detail',
            read_only=True
    )

    class Meta:
        model = Reference
        fields = (
            'id',
            #'url',
            'ref_url',
            'name',
            'user',
            'group'
            )
        #lookup_field = 'user__username'
        extra_kwargs = {
            'group': {'view_name': 'group-detail'},
        }