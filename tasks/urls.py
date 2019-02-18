from django.urls import path, include
from tasks.views import CreatedTaskList, CreatedTaskDetail, TaskCreate, Change_Review

app_name = 'tasks'

urlpatterns = [
    path('task-detail/<slug:slug>/', CreatedTaskDetail.as_view(), name='created-task-detail'),
    path('change-task/<slug:slug>/', CreatedTaskDetail.as_view(), name='change_task'),
    path('change-review/', Change_Review.as_view(), name='change_review'),
    path('create-task/', TaskCreate.as_view(), name='create'),
    path('', CreatedTaskList.as_view(), name='created-tasks'),
]
