from email.mime import application
from django.urls import path, include
from .views import *

app_name = 'club'
urlpatterns = [
    path('freeBoard_index/', freeBoard_index, name='freeBoard_index'),
    path('infoBoard_index/', infoBoard_index, name='infoBoard_index'),
    path('promoBoard_index/', promoBoard_index, name='promoBoard_index'),
    path('notice_index/', notice_index, name='notice_index'),
    path('board_index/<str:topic>/', board_index, name='board_index'),
    path('board_create/<str:topic>/', board_create, name='board_create'),
    path('board_detail/<int:id>/', board_detail, name='board_detail'),
    path('comment_delete/<int:id>', comment_delete, name='comment_delete'),
    path('board_update/<int:id>/', board_update, name='board_update'),
    path('board_delete/<int:id>/', board_delete, name='board_delete'),
    path('event_calendar/', event_calendar, name='event_calendar'),
    path('schedules_sync/', schedules_sync, name='schedules_sync'),
    path('event_thisMonth/', event_thisMonth, name='event_thisMonth'),
    path('club_list/', club_list, name='club_list'),
    path('myClub_list/', myClub_list, name='myClub_list'),
    path('club_home/<str:cName>/', club_home, name='club_home'),
    path('club_board_index/<str:cName>/', club_board_index, name='club_board_index'),
    path('club_board_create/<str:cName>/', club_board_create, name='club_board_create'),
    path('club_application/<str:cName>/', club_application, name='club_application'),
    path('club/club_schedule_index/<str:cName>/', club_schedule_index, name='club_schedule_index'),
    path('club/club_schedule_create/<str:cName>/', club_schedule_create, name='club_schedule_create'),
    path('club/club_schedule_detail/<int:id>/', club_schedule_detail, name='club_schedule_detail'),
    path('club/club_schedule_update/<int:id>/', club_schedule_update, name='club_schedule_update'),
    path('club/club_schedule_delete/<int:id>/', club_schedule_delete, name='club_schedule_delete'),
    path('letter_list/', letter_list, name='letter_list'),
    path('letter_create/', letter_create, name='letter_create'),
    path('letter_detail/<int:id>/', letter_detail, name='letter_detail'),
    path('letter_delete/<int:id>/', letter_delete, name='letter_delete'),
]