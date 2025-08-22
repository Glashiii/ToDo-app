from django.urls import path


from . import views
from .views import delete_task

urlpatterns = [
    path('', views.TaskListCreateView.as_view(), name='tasks_list'),
    path('profile', views.profile, name='profile'),
    path('<int:pk>/toggle/', views.toggle_task_done, name='toggle'),
    path('<int:pk>/delete/', delete_task, name='delete'),
]