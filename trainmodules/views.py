from django.shortcuts import render
from rest_framework import generics
from .models import Type, Module, Assignment
from .serializers import TypeSerializer, ModuleSerializer, AssignmentSerializer, AssignmentDetailSerializer
from userauth.permissions import checkAdmin, checkTrainer, AdminPermission
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


class AssignmentList(generics.ListCreateAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentDetailSerializer

    def get(self, request, *args, **kwargs):
        # todo trainees only can see their assignments
        print(kwargs)
        l = request.user.trainee_assignment_set
        print(l)
        return self.list(request, *args, **kwargs)


class AssignmentCreate(generics.CreateAPIView):
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer
    permission_classes = [AdminPermission]

    def post(self, request, *args, **kwargs):
        print(request.data)
        print(kwargs)
        return self.create(request, *args, **kwargs)


class AssignmentDetail(generics.UpdateAPIView, generics.DestroyAPIView):
    '''
    Both trainer and admin has the permission to change modules
    '''
    queryset = Assignment.objects.all()
    serializer_class = AssignmentSerializer

    def put(self, request, *args, **kwargs):
        res = checkTrainer(request)
        if res is not None:
            return res
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        res = checkTrainer(request)
        if res is not None:
            return res
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        print('delete')
        res = checkTrainer(request)
        if res is not None:
            return res
        return self.destroy(request, *args, **kwargs)
