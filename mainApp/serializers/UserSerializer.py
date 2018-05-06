from rest_framework import serializers
from mainApp.models import User


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
