from django.db import models
from django.contrib.auth.models import User
from autoslug import AutoSlugField
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

class User(AbstractUser):
    is_school = models.BooleanField('school status',default=False)
    is_student = models.BooleanField('student status',default=False)
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='name')
    phone_number = models.CharField(max_length=10)
    email = models.EmailField()

class School(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    address = models.TextField()
    rank = models.IntegerField(blank=True,null=True)
    happiness_score = models.FloatField(blank=True,null=True)
    board = models.CharField(max_length=50)


    def __str__(self) -> str:
        return self.user.name

class Student(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    roll_number = models.CharField(max_length=20)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    

    def __str__(self) -> str:
        return f'{self.school.user.name}: {self.roll_number}'



    
