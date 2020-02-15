from django.urls import path
from trainmodules import views

urlpatterns = [
    path('module/types/', views.TypeList.as_view()),
    path('module/types/<int:pk>/', views.TypeDetail.as_view()),
    path('module/modules/', views.ModuleList.as_view()),
    path('module/modules/<int:pk>/', views.ModuleDetail.as_view()),
    path('module/assignments/', views.AssignmentList.as_view()),
    path('module/assignments/create/', views.AssignmentCreate.as_view()),
    path('module/assignments/<int:pk>/', views.AssignmentDetail.as_view()),

]
