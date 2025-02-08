from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404, HttpResponse
from .models import Chat, ChatMessage
from django.template.loader import render_to_string
import json
from asgiref.sync import async_to_sync

class ChatroomConsumer(WebsocketConsumer):
    def connect(self):       
        self.user = self.scope['user']        
        self.chatroom_id = self.scope['url_route']['kwargs']['chatroom_id']    
        
        try:
            self.chatroom = get_object_or_404(Chat, id = self.chatroom_id)
        except:
            return HttpResponse("Chatroom not found", status=404)
        
        async_to_sync(self.channel_layer.group_add) (
            self.chatroom_id, self.channel_name)

        # add and update online users        
        # if self.user not in self.chatroom.users_online.all():
        #     self.chatroom.users_online.add(self.user)            
        #     self.update_online_count()

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chatroom_id, self.channel_name
        )
        # remove and update online users
        # if self.user in self.chatroom.users_online.all():
        #     self.chatroom.users_online.remove(self.user)
        #     self.update_online_count()

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        body = text_data_json ['body']

        message = ChatMessage.objects.create(
            body = body,
            author = self.user,
            chatroom = self.chatroom
        )
        event = {
            'type':'message_handler',
            'message':message,
        }
        async_to_sync(self.channel_layer.group_send) (
            self.chatroom_id, event)
        
    def message_handler(self, event):
        context = {
            'message':event['message'],
            'user': self.user,
        }        
        html = render_to_string("a_rtchat/partials/chat_message_p.html", context=context)
        self.send(text_data=html)

    # def update_online_count(self):
    #     online_count = self.chatroom.users_online.count() - 1     
    #     event = {
    #         'type':'online_count_handler',
    #         'online_count':online_count
    #     }
    #     async_to_sync(self.channel_layer.group_send) (
    #         self.chatroom_name, event)
        
    # def online_count_handler(self, event):
    #     online_count = event['online_count']
    #     html = render_to_string("a_rtchat/partials/online_count.html", {'online_count':online_count})
    #     self.send(text_data=html)