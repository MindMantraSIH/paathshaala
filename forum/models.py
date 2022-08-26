from enum import unique
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.conf import settings
from autoslug import AutoSlugField


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.CASCADE)
    

class Discussion(models.Model):
    user1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    disc_title = models.CharField(max_length=100)
    #disc_id = models.AutoField()
    disc_content = models.CharField(max_length=5000)
    timestamp= models.DateTimeField(default=now)
    slug = AutoSlugField(populate_from='disc_title', unique=True)
    
class Reply(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)
    reply_id = models.AutoField
    reply_content = models.CharField(max_length=5000) 
    post = models.ForeignKey(Discussion, on_delete=models.CASCADE, default='')
    timestamp= models.DateTimeField(default=now)
    slug = AutoSlugField(populate_from='reply_content', unique=True)

class ForumPost(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=500, blank=True, null=True)
    slug = AutoSlugField(populate_from='title', unique=True)
    content = models.TextField(blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    is_flagged = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.title}'

class ForumComments(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post = models.ForeignKey(ForumPost, on_delete=models.CASCADE, blank=True, null=True)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.post.title}: {self.id}'
