from django.urls import path
from . import views
from .views import *
from rest_framework.authtoken.views import obtain_auth_token
from .views import RegisterView, LoginView ,TaskListCreateView, TaskRetrieveUpdateDestroyView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('tasks/', TaskListCreateView.as_view(), name='task-list-create'),
    path('taskscheck/<int:pk>/', TaskRetrieveUpdateDestroyView.as_view(), name='task-detail'),
]