from django.urls import path
from .views import *

urlpatterns = [
    path('', userchat_view, name='home'),    
    path('chatroom/',chatroom, name="chatroom"),    
    path('new-chatroom/',create_update_chatroom, name="new_chatroom"),
    path('update-chatroom/<uuid:id>',create_update_chatroom, name="update_chatroom"),  
    path('add-member/<uuid:id>',add_member, name="add_member_to_chat"), 
    path('remove-member/<uuid:id>',remove_member, name="remove_member_from_chat"),

    path('chat/room/<uuid:chatroom_id>', chat_view, name='chat'),
    path("chat/room/<uuid:chatroom_id>/set_name/", set_anonymous_name, name="set_anonymous_name"),
]
