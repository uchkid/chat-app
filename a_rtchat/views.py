from django.shortcuts import render, get_object_or_404,redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from .models import ChatRoom, ChatGroup, ChatRoom_Member
from .forms import ChatRoomCreationForm, ChatmessageCreationForm, ChatRoom_MembersCreationForm
from django.urls import reverse

# Create your views here.
def home_view(request):    
    return redirect('accounts/login')

@login_required
def chatroom(request):
    chatrooms= ChatRoom.objects.all().order_by('interview_date')
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
            chatroom = ChatRoom.objects.get(id=id)             
        except ChatRoom.DoesNotExist:
            return HttpResponse("Chatroom not found", status=404) 
       
    if request.method == 'POST':
        chatroom_members_form= ChatRoom_MembersCreationForm(request.POST)           

        if chatroom_members_form.is_valid():
            member = chatroom_members_form.save(commit=False) 
            member.chatroom = chatroom
           
            member.save() 
    else:
        chatroom_members_form = ChatRoom_MembersCreationForm()
    
    chatroom_members = chatroom.chatroom_members.all()
    context = {
        'title':chatroom.title,
        'form': chatroom_members_form, 
        'members':chatroom_members       
    }
    return render(request, 'a_rtchat/addmember.html', context)

@login_required
def create_update_chatroom (request, **kwargs): 
    # print(kwargs)
    # chatroom_id =kwargs.get("id")
    # return HttpResponse(f"Chatroom UUID is {chatroom_id}")
    chatroom_id = kwargs.get("id")
    chatroom = None
    if chatroom_id:
        try:
            chatroom = ChatRoom.objects.get(id=chatroom_id)            
        except ChatRoom.DoesNotExist:
            return HttpResponse("Chatroom not found", status=404)
        update_chatroom = True
    else:
        update_chatroom = False
    
    if request.method == 'POST':
        form = ChatRoomCreationForm(request.POST, instance=chatroom)
        if form.is_valid():
            form.save()
            return redirect('chatroom')
    else:
        form = ChatRoomCreationForm(instance=chatroom)
        
    #update_chatroom =  request.path == reverse('update_chatroom',chatroom_id) if chatroom_id else False
    #print(request.path)
    #print(f'update_chatroom = {update_chatroom}')   
    return render(request, 'a_rtchat/create_chatroom.html', { 'form':form, 'update_chatroom':update_chatroom })   

@login_required
def chat_view(request):    
    chat_group =get_object_or_404(ChatGroup, group_name='public-chat')
    chat_messages = chat_group.chat_messages.all()[:30]
    form = ChatmessageCreationForm()

    #if request.method == 'POST':
    if  request.htmx:
        form = ChatmessageCreationForm(request.POST)
        if form.is_valid:
            message = form.save(commit=False)
            message.author = request.user
            message.group = chat_group
            message.save()
            #return redirect ('home')
            context = {
                'message': message,
                'user':request.user
            }
            return render(request, 'a_rtchat/partials/chat_message_p.html',context)
    return render (request, 'a_rtchat/chat.html', {'chat_messages':chat_messages, 'form':form})
