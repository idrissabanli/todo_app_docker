from django.conf.urls import url
from django.contrib import admin
from users import views

app_name = 'users'

urlpatterns = [
    url(r'^registration', views.user_registration, name='registration'),
]
