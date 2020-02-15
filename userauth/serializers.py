from rest_framework import serializers
from drf_writable_nested.serializers import NestedUpdateMixin
from django.contrib.auth.models import User
from .models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['is_trainer']
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
        fields = '__all__'
        read_only_fields = ['is_superuser']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        '''
        Always create a profile for new user.
        '''
        user = User.objects.create_user(**validated_data)
        try:
            profile_data = validated_data.pop('profile')
            Profile.objects.create(user=user, **profile_data)
        except (KeyError, Profile.DoesNotExist):
            Profile.objects.create(user=user)
        return user
