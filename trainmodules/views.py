from django.shortcuts import render
from rest_framework import generics
from django.contrib.auth.models import User
from .models import Type, Module, Assignment
from .serializers import TypeSerializer, ModuleSerializer, AssignmentSerializer, AssignmentDetailSerializer
from userauth.permissions import checkAdmin, checkTrainer, AdminPermission, TrainerOrAdminPermission, checkTrainerOrAdmin
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND
)
from rest_framework.response import Response
from django.db.models import Q
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
    serializer_class = ModuleSerializer

    def get_queryset(self):
        """
        Optionally restricts the returned purchases to a given user,
        by filtering against a `username` query parameter in the URL.
        """
        queryset = Module.objects.all()
        res = checkTrainerOrAdmin(self.request)
        if res is not None:
            # this is trainee, only can see assigned or public modules
            uid = self.request.user.id
            assignments = Assignment.objects.filter(trainee=uid)
            l = [assignment.module.id for assignment in assignments]
            assigned_modules = Module.objects.filter(pk__in=l)
            public_modules = queryset.filter(privacy='Public')
            queryset = public_modules.union(assigned_modules)
        # filter modules by module type
        module_type = self.request.query_params.get('type', None)
        if module_type is not None:
            try:
                i = int(module_type)
                queryset = queryset.filter(module_type=i)
            except(ValueError):
                queryset = queryset.filter(module_type__name=module_type)
        # filter modules by module id
        pk = self.request.query_params.get('id', None)
        if pk is not None:
            queryset = queryset.filter(id=pk)
        return queryset

    def post(self, request, *args, **kwargs):
        res = checkAdmin(request)
        if res is not None:
            return res
        return self.create(request, *args, **kwargs)


class ModuleDetail(generics.UpdateAPIView, generics.DestroyAPIView):
    '''
    Only admin has the permission to change modules
    '''
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer

    def put(self, request, *args, **kwargs):
        res = checkAdmin(request)
        if res is not None:
            return res
        # when update pass score, need to change the status of related assignment
        pass_score = request.data.get('pass_score', None)
        if pass_score is not None:
            try:
                pk = kwargs.get('pk')
                # make sure module exist
                module = Module.objects.get(id=pk)
                assignments = Assignment.objects.filter(module=pk)
                for assignment in assignments:
                    if assignment.status == 'in progress' and assignment.best_score >= pass_score:
                        assignment.status = 'completed'
                        assignment.save()
                    elif assignment.status == 'completed' and assignment.best_score < pass_score:
                        assignment.status = 'in progress'
                        assignment.save()
            except(KeyError):
                return Response({'error': 'Module not found.'}, HTTP_404_NOT_FOUND)
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
        pk = self.request.query_params.get('id', None)
        if pk is not None:
            queryset = queryset.filter(id=pk)
        return queryset


class AssignmentCreate(generics.CreateAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [TrainerOrAdminPermission]

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
    permission_classes = [TrainerOrAdminPermission]

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
