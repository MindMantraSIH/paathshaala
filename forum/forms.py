from django.forms import ModelForm
from django import forms
from .models import *
from django.contrib.auth.models import User


class DiscussionUpdateForm(forms.ModelForm):
    class Meta:
        model = Discussion
        fields = ['disc_title','disc_content']

class ReplyUpdateForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['reply_content']