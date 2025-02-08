from django.urls import path
from .views import *

urlpatterns = [
    path('', userchat_view, name='home'),
    path('chat/<uuid:chatroom_id>', chat_view, name='chat'),
    path('chatroom/',chatroom, name="chatroom"),    
    path('newchatroom/',create_update_chatroom, name="new_chatroom"),
    path('updatechatroom/<uuid:id>',create_update_chatroom, name="update_chatroom"),  
    path('addmember/<uuid:id>',add_member, name="add_member_to_chat"), 
]
