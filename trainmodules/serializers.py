from rest_framework import serializers
from .models import Module, Assignment, Type
from drf_writable_nested.serializers import NestedUpdateMixin
from userauth.serializers import UserSerializer


class TypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Type
        fields = '__all__'


class ModuleSerializer(NestedUpdateMixin, serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = '__all__'


class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Assignment
        fields = '__all__'


class AssignmentDetailSerializer(serializers.ModelSerializer):
    module = ModuleSerializer()
    trainer = UserSerializer()
    trainee = UserSerializer()

    class Meta:
        model = Assignment
        fields = '__all__'
