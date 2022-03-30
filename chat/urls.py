from django.urls import path
from django.contrib import admin
#from django.conf.urls import url
from django.urls import include, re_path
from .views import *

urlpatterns = [
    re_path(r'^$', index, name='index'),
    re_path(r'^(?P<room_name>[^/]+)/$', room, name='room'),
]