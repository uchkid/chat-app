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
    #my_chatroom = Chat.objects.all().order_by('interview_date')
    #my_chatroom = Chat.objects.filter(created_by = request.user).order_by('interview_date')
    my_chatroom = request.user.chat_admin.all().order_by('interview_date')
    context = {
        'chatrooms': my_chatroom,
    }   
    return render (request, 'a_rtchat/chatroom.html', context)

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
            chatroom = form.save(commit=False)
            chatroom.created_by = request.user
            chatroom.save()
            return redirect('chatroom')
    else:
        form = ChatCreationForm(instance=chatroom) 
    print(f'update chatroom = {update_chatroom}')    
    return render(request, 'a_rtchat/create_chatroom.html', { 'form':form, 'update_chatroom':update_chatroom })   

@login_required
def add_member(request, id): 
    if id:
        try:
            chatroom = Chat.objects.get(id=id)             
        except Chat.DoesNotExist:
            return HttpResponse("Chatroom not found", status=404) 

    if request.method == 'POST':        
        form= ChatRoom_MembersCreationForm(request.POST)           
        
        if form.is_valid():
            members = form.cleaned_data['member']
            for member in members:
                if member not in chatroom.member.all():
                    chatroom.member.add(member)   
            return redirect ('chatroom')         
    else:
        form = ChatRoom_MembersCreationForm(instance=chatroom)
    
    chatroom_members = chatroom.member.all()
    context = {
        'chatroom':chatroom,
        'form': form, 
        'members':chatroom_members       
    }
    return render(request, 'a_rtchat/addmember.html', context)

@login_required
def remove_member(request, id):
    if id:
        try:
            chatroom = Chat.objects.get(id=id)             
        except Chat.DoesNotExist:
            return HttpResponse("Chatroom not found", status=404) 
        
@login_required
def userchat_view(request):
    user_chat =request.user.chat_groups.all()   
    
    return render (request, 'a_rtchat/user_chat.html', {'user_chats':user_chat})

@login_required
def chat_view(request, chatroom_id):
    #return HttpResponse(f"chat with id = {chatroom_id}")    
    if chatroom_id:
        try:
            chatroom = Chat.objects.get(id=chatroom_id)            
        except Chat.DoesNotExist:
            return HttpResponse("Chatroom not found", status=404) 
        
        if request.user in chatroom.member.all():
            chat_messages = chatroom.chat_messages.all()[:30]
            form = ChatmessageCreationForm()
            
            #if request.method == 'POST':
            if  request.htmx:                
                form = ChatmessageCreationForm(request.POST)
                if form.is_valid:
                    message = form.save(commit=False)
                    message.author = request.user
                    message.chatroom = chatroom
                    message.save()                    
                    context = {
                        'message': message,
                        'user':request.user,
                        'chatroom':chatroom
                    }                    
                    return render(request, 'a_rtchat/partials/chat_message_p.html',context)
                    
            return render (request, 'a_rtchat/chat.html', {'chat_messages':chat_messages, 'form':form, 'chatroom':chatroom}) 
        else: 
            return HttpResponse("You are not allowed in this chat", status=404)     
    else:
        return HttpResponse("Chatroom not found", status=404)
    
    