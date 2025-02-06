from django.urls import path
from .views import *

urlpatterns = [
    path('', chat_view, name='home'),
    path('chatroom/',chatroom, name="chatroom"),    
    path('newchatroom/',create_update_chatroom, name="new_chatroom"),
    path('updatechatroom/<uuid:id>',create_update_chatroom, name="update_chatroom"),  
    path('addmember/<uuid:id>',add_member, name="add_member_to_chat"), 
]
