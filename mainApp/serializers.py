from django.contrib.auth.models import User
from rest_framework import serializers

from mainApp.models import Group, Reference


class UserSerializer(serializers.HyperlinkedModelSerializer):
    references = serializers.PrimaryKeyRelatedField(many=True, queryset=Reference.objects.all())

    class Meta:
        model = User
        fields = ('url', 'username', 'first_name', 'last_name', 'email', 'groups', 'references')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('id', 'name', 'priority', 'color')


class ReferenceSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    group = serializers.ReadOnlyField(source='group.id')

    class Meta:
        model = Reference
        fields = ('id', 'url', 'name', 'group', 'user')