from django.urls import path, include
from .views import *

app_name = 'accounts'
urlpatterns = [
    path('signup/', signup, name='signup'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('activate/<str:uidb64>/<str:token>/', activate, name="activate"),
]