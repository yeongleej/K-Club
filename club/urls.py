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
    path('event/', event, name='event'),
    path('club_list/', club_list, name='club_list'),
    path('myClub_list/', myClub_list, name='myClub_list'),
    path('club_home/<str:cName>/', club_home, name='club_home'),
    path('club_application/<str:cName>/', club_application, name='club_application'),
    path('letter_list/', letter_list, name='letter_list'),
    path('letter_create/', letter_create, name='letter_create'),
    path('letter_detail/<int:id>/', letter_detail, name='letter_detail'),
    path('letter_delete/<int:id>/', letter_delete, name='letter_delete'),
]