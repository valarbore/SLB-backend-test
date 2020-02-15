from rest_framework import permissions
from rest_framework.status import (
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND
)
from rest_framework.response import Response
from .models import Profile


class AdminPermission(permissions.BasePermission):
    """
    Check whether user is the admin
    """

    def has_permission(self, request, view):
        return request.user.is_superuser


def checkAdmin(request):
    if request.user.is_superuser is False:
        return Response({"detail": "Authentication credentials were not provided."}, HTTP_401_UNAUTHORIZED)
    return None


def checkTrainer(request):
    try:
        profile = request.user.profile
    except(KeyError, Profile.DoesNotExist):
        return Response({"detail": "Profile not found"}, HTTP_404_NOT_FOUND)
    if profile.is_trainer is False and request.user.is_superuser is False:
        return Response({"detail": "Authentication credentials were not provided."}, HTTP_401_UNAUTHORIZED)
    return None
