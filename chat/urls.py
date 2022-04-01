from django.urls import path
from django.contrib import admin
#from django.conf.urls import url
from django.urls import include, re_path
from .views import *

app_name = 'chat'
urlpatterns = [
    re_path(r'^$', chat_main, name='chat_main'),
    re_path(r'^(?P<room_name>[^/]+)/$', room, name='room'),
]