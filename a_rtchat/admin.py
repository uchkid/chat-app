from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register(ChatGroup)
admin.site.register(GroupMessage)
admin.site.register(ChatRoom)
admin.site.register(ChatRoom_Member)