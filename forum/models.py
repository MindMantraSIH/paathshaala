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

