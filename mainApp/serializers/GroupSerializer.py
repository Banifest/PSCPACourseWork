from rest_framework import serializers
from mainApp.models import Group


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(
            view_name='user-detail',
            read_only=True,
            lookup_field='username'
    )

    class Meta:
        model = Group
        fields = (
            'id',
            'name',
            'priority',
            'color',
            'user'
        )


