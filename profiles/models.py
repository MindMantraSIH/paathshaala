from django.db import models
from django.contrib.auth.models import User
from autoslug import AutoSlugField
from django.utils import timezone
from django.contrib.auth.models import AbstractUser
from django.urls import reverse

class User(AbstractUser):
    is_school = models.BooleanField('school status',default=False)
    is_student = models.BooleanField('student status',default=False)
    is_counselor = models.BooleanField('counselor status', default=False)
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='name')
    phone_number = models.CharField(max_length=10)
    email = models.EmailField()

    def __str__(self) -> str:
        return self.name

class School(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    address = models.TextField()
    rank = models.IntegerField(blank=True,null=True)
    happiness_score = models.FloatField(blank=True,null=True)
    board = models.CharField(max_length=50)
    standard_HI = models.CharField(max_length=100,null=True,blank=True)
    year = models.CharField(max_length=5,null=True)


    def __str__(self) -> str:
        return self.user.name

class Student(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    roll_number = models.CharField(max_length=20)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    std = models.CharField(max_length=10)
    division = models.CharField(max_length=10)
    rewards = models.CharField(max_length=10, blank=True, null=True)


    def __str__(self) -> str:
        return f'{self.school.user.name}: {self.roll_number} : {self.std} : {self.division}'

class Counselor(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    description = models.TextField(null=True, blank=True)
    address = models.TextField(blank=True,null=True)
    pincode = models.CharField(max_length=10, blank=True, null=True)
    speciality = models.CharField(max_length=500, blank=True, null=True)
    awards = models.CharField(max_length=500, blank=True, null=True)
    medical_id_proof = models.FileField(upload_to='counselor/medical_id', null=True, blank=True)
    rating = models.CharField(max_length=10,null=True,blank=True)
    fees = models.CharField(max_length=50, null=True, blank=True)
    latitude = models.CharField(max_length=7, null=True, blank=True)
    longitude = models.CharField(max_length=7, null=True, blank=True)
    is_active = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f'{self.user.name} {(self.speciality)}'
