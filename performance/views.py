from django.shortcuts import render
from rest_framework import generics
from .models import Performance
from .serializers import PerformanceSerializer
from userauth.permissions import checkTrainerOrAdmin
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_401_UNAUTHORIZED,
    HTTP_404_NOT_FOUND
)
from rest_framework.response import Response
from trainmodules.models import Assignment
# Create your views here.


class PerformanceList(generics.ListCreateAPIView):

    serializer_class = PerformanceSerializer

    def get_queryset(self):
        """
        trainee only can see own performance
        """
        queryset = Performance.objects.all()
        res = checkTrainerOrAdmin(self.request)
        if res is not None:
            # this is trainee, only can see assigned or public modules
            uid = self.request.user.id
            queryset = queryset.filter(user=uid)
        # can filter performance according to module/trainee/assignment
        trainee = self.request.query_params.get('trainee', None)
        if trainee is not None:
            queryset = queryset.filter(user=trainee)
        module = self.request.query_params.get('module', None)
        if module is not None:
            queryset = queryset.filter(module=module)
        assignment = self.request.query_params.get('assignment', None)
        if assignment is not None:
            queryset = queryset.filter(assignment=assignment)
        return queryset

    def post(self, request, *args, **kwargs):
        '''
        trainee only can post own performance
        '''
        res = checkTrainerOrAdmin(self.request)
        if res is not None:
            if request.user.id != request.data.get('user'):
                return Response({'error': 'You can not change others performance!'}, HTTP_401_UNAUTHORIZED)
        # check module and user are right for the assignment
        try:
            assignment = Assignment.objects.get(
                id=request.data.get('assignment'))
        except(KeyError, Assignment.DoesNotExist):
            return Response({'error': 'Assignment not found!'}, HTTP_404_NOT_FOUND)
        if assignment.trainee.id != request.data.get('user') or assignment.module.id != request.data.get('module'):
            return Response({'error': 'Module and user do not match assignment!'}, HTTP_400_BAD_REQUEST)
        return self.create(request, *args, **kwargs)


class PerformanceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer

    def get(self, request, *args, **kwargs):
        '''
        trainee only can get own performance
        '''
        res = checkTrainerOrAdmin(request)
        if res is not None:
            try:
                performance = Performance.objects.get(id=kwargs.get('pk'))
            except(KeyError, Performance.DoesNotExist):
                return Response({'error': 'Performance not found!'}, HTTP_404_NOT_FOUND)
            if performance.user.id != request.user.id:
                return Response({'error': 'You can not request others\' performance!'}, HTTP_401_UNAUTHORIZED)
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        '''
        only admin or tainer can update performance
        '''
        res = checkTrainerOrAdmin(request)
        if res is not None:
            return Response({'error': 'You have no permission to update performance!'}, HTTP_401_UNAUTHORIZED)
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        res = checkTrainerOrAdmin(request)
        if res is not None:
            return Response({'error': 'You have no permission to update performance!'}, HTTP_401_UNAUTHORIZED)
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        '''
        trainee only can delete own performance
        '''
        res = checkTrainerOrAdmin(request)
        if res is not None:
            try:
                performance = Performance.objects.get(id=kwargs.get('pk'))
            except(KeyError, Performance.DoesNotExist):
                return Response({'error': 'Performance not found!'}, HTTP_404_NOT_FOUND)
            if performance.user.id != request.user.id:
                return Response({'error': 'You can not delete others\' performance!'}, HTTP_401_UNAUTHORIZED)
        return self.destroy(request, *args, **kwargs)
