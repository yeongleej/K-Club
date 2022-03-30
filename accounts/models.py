from django.db import models
from django.contrib.auth.models import User, AbstractUser

# Create your models here.
class Member(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    student_num = models.IntegerField(default=0)
    email = models.EmailField(max_length=255, unique=True, default='')
    #password = models.CharField(max_length=255)
    phone_num = models.CharField(max_length=255)
    is_auth = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'member'
