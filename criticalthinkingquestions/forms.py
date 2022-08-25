from django.forms import ModelForm
from django import forms
from .models import *
from django.contrib.auth.models import User


class quesUpdateForm(forms.ModelForm):
    class Meta:
        model = Brainstorm
        fields = ['disc_title']

class RepliesUpdateForm(forms.ModelForm):
    class Meta:
        model = Replies
        fields = ['reply_content']