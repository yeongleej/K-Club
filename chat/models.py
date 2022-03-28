from django.db import models
from club.models import Club
from account.models import Member
# Create your models here.

class Chat(models.Model):
    club_id = models.ForeignKey(Club, on_delete=models.CASCADE)
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE)
    content = models.TextField(max_length=1000, blank=True)
    
    class Meta:
        db_table = 'chat' 
