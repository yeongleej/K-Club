from django.db import models
#import accounts.models
from datetime import datetime
from accounts.models import *

# Create your models here.
class Club(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    member = models.ForeignKey('accounts.Member', on_delete=models.CASCADE)
    is_manager = models.BooleanField(default=False)
    #field = models.CharField(max_length=100)
    # description = models.TextField(max_length=1000, blank=True)
    image_url = models.ImageField(blank=True)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'club'

class Club_Info(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(max_length=1000, blank=True)
    field = models.CharField(max_length=100, blank=True, null=True)
    image_url = models.ImageField(upload_to='images/',blank=True, null=True)
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'club_info'

class Board(models.Model):
    id = models.AutoField(primary_key=True)
    member = models.ForeignKey('accounts.Member', on_delete=models.CASCADE)
    club_name = models.CharField(max_length=100, blank=True)
    topic = models.CharField(max_length=100, blank=False)
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=1000, blank=True)
    written_at = models.DateTimeField(auto_now_add=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'Board'

class Comment(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    board = models.ForeignKey(Board, null=False, blank=False, on_delete=models.CASCADE)
    member = models.ForeignKey('accounts.Member', null=False, blank=False, on_delete=models.CASCADE)
    written_at = models.DateField(auto_now_add=True, null=False, blank=False)
    comment = models.TextField()

    def __str__(self):
        return self.comment
    class Meta:
        db_table = 'Comment'

class Application(models.Model):
    id = models.AutoField(primary_key=True)
    club_name = models.CharField(max_length=100)
    member = models.ForeignKey('accounts.Member', on_delete=models.CASCADE)

    class Meta:
        db_table = 'Application'

class Letter(models.Model):
    id = models.AutoField(primary_key=True, null=False, blank=False)
    title = models.CharField(max_length=100)
    content = models.TextField()
    from_member_name = models.CharField(max_length=100)
    to_member_name =models.CharField(max_length=100)
    written_at = models.DateField(auto_now_add=True, null=False, blank=False)
    reference_id = models.IntegerField(default=0, blank=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.title
    class Meta:
        db_table = 'Letter'

class Todo(models.Model):
    id = models.AutoField(primary_key=True)
    content = models.TextField(max_length=1000, blank=True)
    club_name = models.CharField(max_length=100)
    is_checked = models.BooleanField(default=False, null = True)
    def __str__(self):
        return self.content
    class Meta:
        db_table = 'Todo'

class Schedule(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, blank=True, null = True)
    start_at = models.DateField(default=datetime.now)
    finish_at = models.DateField(default=datetime.now)
    content = models.TextField(max_length=1000, blank=True)
    state = models.TextField(max_length=100, blank=True, null = True)
    club_name = models.CharField(max_length=100)
    image_url = models.ImageField(upload_to='images/',blank=True, null=True)
    def __str__(self):
        return self.content
    
    class Meta:
        db_table = 'schedule'