from django.forms import ModelForm
from django import forms
from .models import *

class ChatmessageCreationForm(ModelForm):
    class Meta:
        model = GroupMessage
        fields = ['body']
        widgets = {
            'body':forms.TextInput(attrs={'placeholder': 'Add message ...', 'class':'p-4 text-black', 
                                          'maxlength':300, 'autofocus':True}),
        }

class ChatRoomCreationForm(ModelForm):
    class Meta:
        model = ChatRoom
        fields = ['title', 'interview_date', 'interview_time','company_name', 'vendor_name']
        labels = {
            "title": "Interview Title",
            "interview_date": "Interview Date",
            "interview_time": "Interview Time",
            "company_name": "Company Name",
            "vendor_name": "Vendor Information",
        }
        widgets = { 
            'title':forms.TextInput(attrs={'placeholder': 'Add message ...', 'class':'p-4 text-black', 
                                          'maxlength':300, 'autofocus':True}),
            'interview_date':forms.DateInput(attrs={"type": "date"}),
            'interview_time':forms.TimeInput(attrs={"type": "time"}),           
            'company_name' : forms.TextInput(attrs={'placeholder': 'Add compnay'}),
            'vendor_name' : forms.TextInput(attrs={'placeholder': 'add vendor'})
        }
        
class ChatRoom_MembersCreationForm(ModelForm):
    class Meta:
        model = ChatRoom_Member      
        fields = ['participant']