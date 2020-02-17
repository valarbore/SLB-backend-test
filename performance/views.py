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


def updateScore(assignment, request):
    # when create/update performance, update the best score and assignemnt status
    newscore = int(request.data.get('score', 0))
    if newscore >= assignment.best_score:
        assignment.best_score = newscore
        assignment.save()
    if assignment.status == 'in progress' and assignment.best_score >= assignment.module.pass_score:
        assignment.status = 'completed'
        assignment.save()


class PerformanceList(generics.ListCreateAPIView):

    serializer_class = PerformanceSerializer

    def get_queryset(self):
        """
        trainee only can see own performance
        """
        queryset = Performance.objects.all()
        res = checkTrainerOrAdmin(self.request)
        if res is not None:
            # this is trainee, only can see own performance
            uid = self.request.user.id
            queryset = queryset.filter(assignment__trainee=uid)
        # can filter performance according to module/trainee/assignment
        trainee = self.request.query_params.get('trainee', None)
        if trainee is not None:
            queryset = queryset.filter(assignment__trainee=trainee)
        trainer = self.request.query_params.get('trainer', None)
        if trainer is not None:
            queryset = queryset.filter(assignment__trainer=trainer)
        module = self.request.query_params.get('module', None)
        if module is not None:
            queryset = queryset.filter(assignment__module=module)
        assignment = self.request.query_params.get('assignment', None)
        if assignment is not None:
            queryset = queryset.filter(assignment__id=assignment)
        return queryset

    def post(self, request, *args, **kwargs):
        '''
        trainee only can post own performance
        '''
        try:
            assignment = Assignment.objects.get(
                id=request.data.get('assignment'))
        except(KeyError, Assignment.DoesNotExist):
            return Response({'error': 'Assignment not found!'}, HTTP_404_NOT_FOUND)
        res = checkTrainerOrAdmin(self.request)
        if res is not None:
            # this is a trainee only can create performance for own assignment
            if request.user.id != assignment.trainee.id:
                return Response({'error': 'You can not change others performance!'}, HTTP_401_UNAUTHORIZED)
        # update best score and assignment status
        updateScore(assignment, request)
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
            if performance.assignment.trainee.id != request.user.id:
                return Response({'error': 'You can not request others\' performance!'}, HTTP_401_UNAUTHORIZED)
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        '''
        only admin or tainer can update performance
        '''
        res = checkTrainerOrAdmin(request)
        if res is not None:
            return Response({'error': 'You have no permission to update performance!'}, HTTP_401_UNAUTHORIZED)
        try:
            assignment = Assignment.objects.get(id=kwargs.get('pk'))
            # update best score and assignment status
            updateScore(assignment, request)
        except(KeyError):
            pass
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        res = checkTrainerOrAdmin(request)
        if res is not None:
            return Response({'error': 'You have no permission to update performance!'}, HTTP_401_UNAUTHORIZED)
        try:
            assignment = Assignment.objects.get(id=kwargs.get('pk'))
            # update best score and assignment status
            updateScore(assignment, request)
        except(KeyError):
            pass
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
            if performance.assignment.trainee.id != request.user.id:
                return Response({'error': 'You can not delete others\' performance!'}, HTTP_401_UNAUTHORIZED)
        return self.destroy(request, *args, **kwargs)
