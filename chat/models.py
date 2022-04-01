from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

# class Chat(models.Model):
#     id = models.AutoField(primary_key=True)
#     club_id = models.ForeignKey(Club, on_delete=models.CASCADE)
#     member_id = models.ForeignKey(Member, on_delete=models.CASCADE)
#     content = models.TextField(max_length=1000, blank=True)
    
#     class Meta:
#         db_table = 'chat' 

# class ChatRoom(models.Model):
#     id = models.AutoField(primary_key=True)
#     roomName = models.CharField(max_length=100, unique=True)

#     def __str__(self):
#         return self.roomName
#     class Meta:
#         db_table = 'chatRoom'

User = get_user_model()

class Message(models.Model):
    author = models.ForeignKey(User, related_name='author_messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    room = models.CharField(max_length=100, null=True, blank=True)
    def __str__(self):
        return self.author.username
    def last_10_messages():
        return Message.objects.order_by('timestamp')[:10]
    
    class Meta:
        db_table = 'message'
