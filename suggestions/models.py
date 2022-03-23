from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.conf import settings
from autoslug import AutoSlugField
from profiles.models import School


class Data(models.Model):
    school = models.ForeignKey(School, on_delete=models.CASCADE, default=1)
    levelc = models.IntegerField(max_length=100)
    disc_content = models.CharField(max_length=5000)
    timestamp= models.DateTimeField(default=now)
    slug = AutoSlugField(populate_from='disc_title', unique=True)