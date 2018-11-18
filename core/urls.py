from django.urls import path, include
from core.views import DesktopView
from core.views import TaskReviewView
from django.urls import re_path

app_name = 'core'

urlpatterns = [
    path('', DesktopView.as_view()),
    path('task-reviews/<int:pk>/', TaskReviewView.as_view(), name='task-reviews'),
]