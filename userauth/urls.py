from django.urls import path
from userauth import views

urlpatterns = [
    path('auth/login/', views.login),
    path('auth/logout/', views.logout),
    path('auth/changerole/', views.changeRole),
    path('auth/users/<int:pk>/', views.UserDetail.as_view()),
    path('auth/users/', views.UserList.as_view()),
    path('auth/users/create/', views.CreateUser.as_view()),

]
