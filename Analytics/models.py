from django.db import models
from django.contrib.auth.models import User
from autoslug import AutoSlugField
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from profiles.models import School

# Create your models here.

class Academics(models.Model):
    school = models.OneToOneField(School,on_delete=models.CASCADE,primary_key=True)
    name = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    english = models.IntegerField(blank=True,null=True)


