from django.urls import path, include
from .views import task_list, TaskView, TaskCreateView, ReportCreateView, ProfileView

app_name = 'home'
urlpatterns = [
    path('', task_list, name='list_task'),
    path('task/<int:pk>', TaskView.as_view(), name='task_view'),
    path('task/create/', TaskCreateView.as_view(), name='task_create'),
    path('report/create/', ReportCreateView.as_view(), name='report_create'),
    path('profile/', ProfileView.as_view(), name='profile'),


    
]