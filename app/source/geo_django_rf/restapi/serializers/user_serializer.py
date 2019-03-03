from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = get_user_model()
        fields = (
            'url',
            'created_at',
            'updated_at',
            'username',
            'email',
            'password',
            'groups',
            'profile',
        )

    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[UniqueValidator(queryset=get_user_model().objects.all())]
    )
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=get_user_model().objects.all())]
    )
    password = serializers.CharField(min_length=8, write_only=True)
    created_at = serializers.DateTimeField(read_only=True, source='date_joined')
    updated_at = serializers.DateTimeField(read_only=True)
    profile = serializers.HyperlinkedRelatedField(read_only=True, view_name='profile-detail')

    def create(self, validated_data):
        return get_user_model().objects.create_user(
            validated_data['username'], validated_data['email'], validated_data['password']
        )
