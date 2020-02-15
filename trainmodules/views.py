from django.shortcuts import render
from rest_framework import generics
from django.contrib.auth.models import User
from .models import Type, Module, Assignment
from .serializers import TypeSerializer, ModuleSerializer, AssignmentSerializer, AssignmentDetailSerializer
from userauth.permissions import checkAdmin, checkTrainer, AdminPermission, TrainerPermission, checkTrainerOrAdmin
from rest_framework.status import (
    HTTP_400_BAD_REQUEST
)
from rest_framework.response import Response
# Create your views here.


class TypeList(generics.ListCreateAPIView):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer

    def post(self, request, *args, **kwargs):
        res = checkAdmin(request)
        if res is not None:
            return res
        return self.create(request, *args, **kwargs)


class TypeDetail(generics.RetrieveUpdateDestroyAPIView):
    '''
    Only admin has the permission to change type
    '''
    queryset = Type.objects.all()
    serializer_class = TypeSerializer

    def put(self, request, *args, **kwargs):
        res = checkAdmin(request)
        if res is not None:
            return res
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        res = checkAdmin(request)
        if res is not None:
            return res
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        res = checkAdmin(request)
        if res is not None:
            return res
        return self.destroy(request, *args, **kwargs)


class ModuleList(generics.ListCreateAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer

    def post(self, request, *args, **kwargs):
        res = checkAdmin(request)
        if res is not None:
            return res
        return self.create(request, *args, **kwargs)


class ModuleDetail(generics.RetrieveUpdateDestroyAPIView):
    '''
    Only admin has the permission to change modules
    '''
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer

    def put(self, request, *args, **kwargs):
        res = checkAdmin(request)
        if res is not None:
            return res
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        res = checkAdmin(request)
        if res is not None:
            return res
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        res = checkAdmin(request)
        if res is not None:
            return res
        return self.destroy(request, *args, **kwargs)


class AssignmentList(generics.ListAPIView):
    serializer_class = AssignmentDetailSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Assignment.objects.all()
        res = checkTrainerOrAdmin(self.request)
        if res is not None:
            # this is trainee, only can see own assignments
            queryset = queryset.filter(trainee=self.request.user.id)
        else:
            # trainer or admin can see all the assignments or search for
            # specific trainer/module/trainee
            trainer = self.request.query_params.get('trainer', None)
            if trainer is not None:
                queryset = queryset.filter(trainer=trainer)
            trainee = self.request.query_params.get('trainee', None)
            if trainee is not None:
                queryset = queryset.filter(trainee=trainee)
            module = self.request.query_params.get('module', None)
            if module is not None:
                queryset = queryset.filter(module=module)
        return queryset


class AssignmentCreate(generics.CreateAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [AdminPermission]

    def post(self, request, *args, **kwargs):
        # check whether trainer is a trainer
        res = checkTrainer(request)
        if res is not None:
            return res
        return self.create(request, *args, **kwargs)


class AssignmentDetail(generics.UpdateAPIView, generics.DestroyAPIView):
    '''
    Both trainer and admin has the permission to change modules
    '''
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [TrainerPermission]

    def put(self, request, *args, **kwargs):
        # if update trainer check whether trainer is a trainer
        # check whether trainer is a trainer
        res = checkTrainer(request)
        if res is not None:
            return res
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        # todo if update trainer check whether trainer is a trainer
        res = checkTrainer(request)
        if res is not None:
            return res
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
