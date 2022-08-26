from enum import unique
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.conf import settings
from autoslug import AutoSlugField


class BrainstormingProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    

class Brainstorm(models.Model):
    user1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    disc_title = models.CharField(max_length=100)
    timestamp= models.DateTimeField(default=now)
    slug = AutoSlugField(populate_from='disc_title', unique=True)
    
class Replies(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    reply_id = models.AutoField
    reply_content = models.CharField(max_length=5000) 
    post = models.ForeignKey(Brainstorm, on_delete=models.CASCADE, default='')
    timestamp= models.DateTimeField(default=now)
    slug = AutoSlugField(populate_from='reply_content', unique=True)

class quesPost(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=500, blank=True, null=True)
    slug = AutoSlugField(populate_from='title', unique=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.title}'

class quesComments(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(quesPost, on_delete=models.CASCADE, blank=True, null=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.post.title}: {self.id}'
