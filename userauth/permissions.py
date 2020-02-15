from rest_framework import permissions
from rest_framework.status import (
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND
)
from rest_framework.response import Response
from .models import Profile
from django.contrib.auth.models import User


class AdminPermission(permissions.BasePermission):
    """
    Check whether user is the admin
    """

    def has_permission(self, request, view):
        return request.user.is_superuser


class TrainerPermission(permissions.BasePermission):
    """
    Check whether user is the admin
    """

    def has_permission(self, request, view):
        try:
            profile = request.user.profile
        except(KeyError, Profile.DoesNotExist):
            return False
        return request.user.is_superuser or profile.is_trainer


def checkAdmin(request):
    if request.user.is_superuser is False:
        return Response({"detail": "Authentication credentials were not provided."}, HTTP_401_UNAUTHORIZED)
    return None


def checkTrainerOrAdmin(request):
    try:
        profile = request.user.profile
    except(KeyError, Profile.DoesNotExist):
        return Response({"detail": "Profile not found"}, HTTP_404_NOT_FOUND)
    if profile.is_trainer is False and request.user.is_superuser is False:
        return Response({"detail": "Authentication credentials were not provided."}, HTTP_401_UNAUTHORIZED)
    return None


def checkTrainer(request):
    trainer = request.data['trainer']
    if trainer is not None:
        user = User.objects.get(id=trainer)
        if user.profile.is_trainer is False:
            return Response({'error': 'You can not assign a user as trainer who is not a trainer!'}, HTTP_400_BAD_REQUEST)
    return None
