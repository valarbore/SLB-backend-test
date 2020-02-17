from rest_framework import serializers
from drf_writable_nested.serializers import NestedUpdateMixin
from django.contrib.auth.models import User
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['is_trainer', 'avatar']
        read_only_fields = ['is_trainer']


class UserSerializer(NestedUpdateMixin, serializers.ModelSerializer):
    profile = ProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email',
                  'profile', 'is_superuser']
        read_only_fields = ['is_superuser']


class CreateUserSerializer(NestedUpdateMixin, serializers.ModelSerializer):
    profile = ProfileSerializer(required=False)

    class Meta:
        model = User
        fields = ['id', 'username', 'email',
                  'profile', 'is_superuser', 'password']
        read_only_fields = ['is_superuser']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        '''
        Always create a profile for new user.
        '''
        profile_data = None
        try:
            profile_data = validated_data.pop('profile')
        except():
            pass
        user = User.objects.create_user(**validated_data)
        if profile_data is not None:
            Profile.objects.create(user=user, **profile_data)
        else:
            Profile.objects.create(user=user)
        return user
