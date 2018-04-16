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
        fields = ('name', 'priority', 'color')


class ReferenceSerializer(serializers.HyperlinkedModelSerializer):
    snippets = serializers.HyperlinkedRelatedField(
        many=True, view_name='snippet-detail', read_only=True)

    class Meta:
        model = Reference
        fields = ('url', 'id', 'name', 'group')