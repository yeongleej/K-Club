from django.db import models
from account.models import Member
from datetime import datetime

# Create your models here.
class Club(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(max_length=1000, blank=True)
    image_url = models.ImageField(blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'club'

class Article(models.Model):
    member_id = models.ForeignKey(Member, on_delete=models.CASCADE)
    club_id = models.ForeignKey(Club, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=1000, blank=True)
    written_at = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'article'

class Todo(models.Model):
    content = models.TextField(max_length=1000, blank=True)
    club_id = models.ForeignKey(Club, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'Todo'

class Schedule(models.Model):
    start_at = models.DateField(default=datetime.now)
    finish_at = models.DateField(default=datetime.now)
    content = models.TextField(max_length=1000, blank=True)
    club_id = models.ForeignKey(Club, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'schedule'