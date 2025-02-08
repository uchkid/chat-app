from django.shortcuts import render, get_object_or_404,redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Chat
from .forms import ChatCreationForm, ChatmessageCreationForm, ChatRoom_MembersCreationForm
from django.urls import reverse

# Create your views here.
def home_view(request):    
    return redirect('accounts/login')

@login_required
def chatroom(request):
    chatrooms= Chat.objects.all().order_by('interview_date')
    context = {
        'chatrooms': chatrooms,
    }
    return render (request, 'a_rtchat/chatroom.html', context)

@login_required
def add_member(request, id):    
    members = None
    chatroom = None
    if id:
        try:
            chatroom = Chat.objects.get(id=id)             
        except Chat.DoesNotExist:
            return HttpResponse("Chatroom not found", status=404) 
       
    if request.method == 'POST':
        chatroom_members_form= ChatRoom_MembersCreationForm(request.POST)           

        if chatroom_members_form.is_valid():
            member = chatroom_members_form.save(commit=False) 
            member.chatroom = chatroom
           
            member.save() 
    else:
        chatroom_members_form = ChatRoom_MembersCreationForm()
    
    chatroom_members = chatroom.chatroom.all()
    context = {
        'title':chatroom.title,
        'form': chatroom_members_form, 
        'members':chatroom_members       
    }
    return render(request, 'a_rtchat/addmember.html', context)

@login_required
def create_update_chatroom (request, **kwargs): 
    chatroom_id = kwargs.get("id")
    chatroom = None
    if chatroom_id:
        try:
            chatroom = Chat.objects.get(id=chatroom_id)            
        except Chat.DoesNotExist:
            return HttpResponse("Chatroom not found", status=404)
        update_chatroom = True
    else:
        update_chatroom = False
    
    if request.method == 'POST':
        form = ChatCreationForm(request.POST, instance=chatroom)
        if form.is_valid():
            form.save()
            return redirect('chatroom')
    else:
        form = ChatCreationForm(instance=chatroom) 
        
    return render(request, 'a_rtchat/create_chatroom.html', { 'form':form, 'update_chatroom':update_chatroom })   

@login_required
def userchat_view(request):  
    user = request.user  
    user_chat =Chat.objects.filter(chatroom__participant=user) 
    user_participant = request.user.chatroom_participant.all()
    print(user_participant)
    print(user_chat)
    
    return render (request, 'a_rtchat/user_chat.html', {'user_chats':user_chat})

@login_required
def chat_view(request, chatroom_id):
    return HttpResponse(f"chat with id = {chatroom_id}")