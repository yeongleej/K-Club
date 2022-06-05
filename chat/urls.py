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

# re_path
# ^: 정규식 시작 기호
# $: 정규식 종료 기호
# r: 이스케이프 기호
# (?P<파라미터명>정규식패턴)