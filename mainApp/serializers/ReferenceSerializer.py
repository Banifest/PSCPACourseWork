from rest_framework import serializers

from mainApp.models import Group, Reference


class ReferenceSerializer(serializers.HyperlinkedModelSerializer):
    user = serializers.HyperlinkedRelatedField(
            view_name='user-detail',
            read_only=True,
            lookup_field='username'
    )

    group = serializers.SlugRelatedField(
        slug_field='id',
        read_only=False,
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