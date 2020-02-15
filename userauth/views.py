from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate
from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK,
    HTTP_401_UNAUTHORIZED
)
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import UserSerializer, ProfileSerializer, CreateUserSerializer
from .models import Profile
from rest_framework import generics
from .permissions import AdminPermission, checkTrainerOrAdmin


@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):
    '''
    login through username and password and return a token if success
    '''
    username = request.data.get("username")
    password = request.data.get("password")
    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)
    user = authenticate(username=username, password=password)
    if not user:
        return Response({'error': 'Invalid Credentials'},
                        status=HTTP_404_NOT_FOUND)
    # admin created by command-line need to create a profile for it
    if user.is_superuser:
        try:
            user.profile
        except(KeyError, Profile.DoesNotExist):
            Profile.objects.create(user=user)
    token, _ = Token.objects.get_or_create(user=user)
    return Response({'token': token.key},
                    status=HTTP_200_OK)


def findUser(request):
    '''
    Try to find user according to uid or username
    '''
    username = request.data.get("username")
    uid = request.data.get("uid")
    if username is None and uid is None:
        return Response({'error': 'Please provide username or uid'},
                        status=HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get_by_natural_key(
            username) if username else User.objects.get(id=uid)
    except(KeyError, User.DoesNotExist):
        return Response({'error': 'Not found.'},
                        status=HTTP_404_NOT_FOUND)
    return user


@csrf_exempt
@api_view(["PUT"])
@permission_classes((AdminPermission,))
def changeRole(request):
    '''
    Admin can change users role through their username or uid
    '''
    user = findUser(request)
    if isinstance(user, Response):
        return user
    is_trainer = request.data.get("is_trainer")
    is_superuser = request.data.get("is_superuser")
    profile = user.profile
    if is_trainer is not None:
        profile.is_trainer = bool(is_trainer)
    if is_superuser is not None:
        user.is_superuser = bool(is_superuser)
    profile.save()
    user.save()
    return Response(UserSerializer(user).data,
                    status=HTTP_200_OK)


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def delete(self, request, *args, **kwargs):
        '''
        Only admin can delete user
        '''
        res = checkTrainerOrAdmin(request)
        if res is not None:
            return res
        return self.destroy(request, *args, **kwargs)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CreateUser(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
