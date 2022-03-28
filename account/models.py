from django.db import models

# Create your models here.
class Member(models.Model):
    name = models.CharField(max_length=100)
    student_num = models.IntegerField(default=0)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    phone_num = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'member'