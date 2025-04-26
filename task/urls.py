from django.urls import path, include
from .views import task_list, TaskView, TaskCreateView

app_name = 'home'
urlpatterns = [
    path('', task_list, name='list_task'),
    path('task/<int:pk>', TaskView.as_view(), name='task_view'),
    path('task/create/', TaskCreateView.as_view(), name='task_create')


    
]