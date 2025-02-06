from django.db import models
from django.contrib.auth.models import User
#from django.contrib.auth import get_user_model
from a_common.models import TimeStampedModel
import uuid

# Create your models here.
class ChatGroup(models.Model):
    group_name = models.CharField(max_length=128, unique = True)
    #users_online= models.ManyToManyField(User, related_name='online_in_groups',blank=True)

    def __str__(self):
        return self.group_name
    
class GroupMessage(models.Model):
    group = models.ForeignKey(ChatGroup, related_name='chat_messages', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    body = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author.username} : {self.body}'
    
    class Meta:
        ordering = ['created']

class ChatRoom(TimeStampedModel):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(verbose_name=("Title"), max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    interview_date = models.DateField()
    interview_time = models.TimeField()
    company_name = models.CharField(verbose_name=("Company Name"), max_length=255)
    vendor_name = models.CharField(verbose_name=("Vendor Name"), max_length=255)

    def __str__(self):
        return self.title

class ChatRoom_Member(models.Model):
    chatroom = models.ForeignKey(ChatRoom, related_name='chatroom_members', on_delete=models.CASCADE)
    participant = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    class Meta:
        unique_together = ('chatroom','participant')


