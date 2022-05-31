from django.urls import path, include
from .views import *

app_name = 'accounts'
urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('activate/<str:uidb64>/<str:token>/', activate, name="activate"),
    path('password_check/', password_check, name='password_check'),
    path('mypage/', mypage, name='mypage'),
    path('mypage/application_list/<str:cName>/', application_list, name='application_list'),
    path('mypage/club_member_management/<str:cName>/', club_member_management, name='club_member_management'),
    path('mypage/club_resign/<int:id>/', club_resign, name='club_resign'),
]