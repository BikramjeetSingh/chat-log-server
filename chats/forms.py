from django import forms


class ChatLogForm(forms.Form):

    content = forms.CharField(required=True)
    timestamp = forms.IntegerField(required=True)
    is_sent = forms.BooleanField(required=True)

