from django.urls import path, include
from tasks.views import CreatedTaskList, TaskList, CreatedTaskDetail, ShareTask, TaskCreate

app_name = 'tasks'

urlpatterns = [
    path('task-detail/<slug:slug>/', CreatedTaskDetail.as_view(), name='created-task-detail'),
    path('share-task/<slug:slug>/', ShareTask.as_view(), name='share-task'),
    path('created/', CreatedTaskList.as_view(), name='created-tasks'),
    path('create-task/', TaskCreate.as_view(), name='create'),
    path('', TaskList.as_view(), name='shared_task'),
]
