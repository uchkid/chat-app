from django.db import models
from django.contrib.auth.models import User
#from django.contrib.auth import get_user_model
from a_common.models import TimeStampedModel
import uuid

class Chat(TimeStampedModel):
    pkid = models.BigAutoField(primary_key=True, editable=False)
    id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title = models.CharField(verbose_name=("Title"), max_length=255)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='chat_admin')
    interview_date = models.DateField()
    interview_time = models.TimeField()
    company_name = models.CharField(verbose_name=("Company Name"), max_length=255)
    vendor_name = models.CharField(verbose_name=("Vendor Name"), max_length=255)
    is_private = models.BooleanField(default=False)
    member = models.ManyToManyField(User, related_name='chat_groups', blank=True)
    users_online= models.ManyToManyField(User, related_name='online_in_groups',blank=True)

    def __str__(self):
        return self.title

class ChatMessage(models.Model):
    chatroom = models.ForeignKey(Chat, related_name='chat_messages', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    body = models.CharField(max_length=300)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author.username} : {self.body}'
    
    class Meta:
        ordering = ['created']



