from django.db import models
from django.contrib.auth.models import User
from autoslug import AutoSlugField
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.urls import reverse
from profiles.models import School, Student

# Create your models here.

class Academics(models.Model):
    school = models.ForeignKey(School,on_delete=models.CASCADE)
    student = models.ForeignKey(Student,on_delete=models.CASCADE, blank=True, null=True)
    roll_no = models.CharField(max_length=500, primary_key= True)
    name = models.CharField(max_length=50)
    standard = models.CharField(max_length=3)
    division = models.CharField(max_length=3)
    english = models.FloatField(blank=True,null=True)
    hindi = models.FloatField(blank=True,null=True)
    maths = models.FloatField(blank=True, null=True)
    science = models.FloatField(blank=True, null=True)
    history = models.FloatField(blank=True,null=True)
    geo = models.FloatField(blank=True,null=True)
    percent = models.FloatField(blank=True, null=True)
    interactivity = models.FloatField(blank=True, null=True)
    timely_submissions = models.FloatField(blank=True,null=True)
    attentiveness = models.FloatField(blank=True,null=True)
    creativity = models.FloatField(blank=True, null=True)
    participation = models.FloatField(blank=True, null=True)
    confidence = models.FloatField(blank=True,null=True)
    social_relationship = models.FloatField(blank=True,null=True)
    obedience = models.FloatField(blank=True, null=True)


