from django.db import models
from django.contrib.auth.models import User, AbstractUser
from club.models import Club


# Create your models here.
class Member(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    student_num = models.CharField(max_length=100, unique=True)
    major = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True, default='')
    phone_num = models.CharField(max_length=255)
    is_auth = models.BooleanField(default=False)
    #club_name = models.CharField(max_length=100, blank=True)
    #room = models.CharField(max_length=100, null=True, blank=True) # 가장 최근의 채팅방

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'member'
