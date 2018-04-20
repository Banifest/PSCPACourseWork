from rest_framework import serializers

from mainApp.models import Group, Reference, User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    # refs = serializers.HyperlinkedRelatedField(
    #         read_only=True,
    #         many=True,
    #         view_name='user-refs'
    # )

    class Meta:
        model = User
        fields = ('url',
                  'username',
                  'first_name',
                  'last_name',
                  'email',
                  'references',
                  'groups',
                  #'refs'
                  )


class GroupSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Group
        fields = ('url', 'id', 'name', 'priority', 'color')


class ReferenceSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Reference
        fields = ('id', 'url', 'name', 'user', 'group')
        extra_kwargs = {
            'group': {'view_name': 'group-detail'},
        }