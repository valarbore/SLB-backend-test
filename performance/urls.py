from django.urls import path
from performance import views

urlpatterns = [
    path('performances/', views.PerformanceList.as_view()),
    path('performances/<int:pk>/', views.PerformanceDetail.as_view())
]
