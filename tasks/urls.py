from django.urls import path, include
from tasks.views import CreatedTaskList, CreatedTaskDetail, TaskCreate

app_name = 'tasks'

urlpatterns = [
    path('task-detail/<slug:slug>/', CreatedTaskDetail.as_view(), name='created-task-detail'),
    path('create-task/', TaskCreate.as_view(), name='create'),
    path('', CreatedTaskList.as_view(), name='created-tasks'),
]
