from django import forms
from .models import Message
from account.models import CustomUser

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['receiver', 'subject', 'body']
        widgets = {
            'body': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Type your message here...'}),
        }

    def __init__(self, *args, **kwargs):
        self.sender = kwargs.pop('sender', None)
        super().__init__(*args, **kwargs)
        if self.sender:
            self.fields['receiver'].queryset = CustomUser.objects.exclude(id=self.sender.id)