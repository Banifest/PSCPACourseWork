from rest_framework import serializers
from rest_framework.relations import HyperlinkedIdentityField
from rest_framework_nested.relations import NestedHyperlinkedRelatedField

from mainApp.models import Group, Reference, User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    url = serializers.HyperlinkedIdentityField(
            view_name='user-detail',
            lookup_field='username'
    )
    class Meta:
        model = User
        fields = (
            'url',
            'username',
            'first_name',
            'last_name',
            'email',
        )


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


class ReferenceSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(
            view_name='user-detail',
            read_only=True,
            lookup_field='username'
    )

    group = serializers.SlugRelatedField(
        slug_field='id',
        read_only=False,  # Or add a queryset
        queryset=Group.objects.filter().all()
    )

    class Meta:
        model = Reference
        fields = (
            'id',
            'ref_url',
            'name',
            'user',
            'group'
        )
