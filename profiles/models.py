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
    rank = models.IntegerField(blank=True)
    board = models.CharField(max_length=50)


    def __str__(self) -> str:
        return self.user.name

class Student(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    roll_number = models.CharField(max_length=20)
    school = models.OneToOneField(School, on_delete=models.CASCADE)
    

    def __str__(self) -> str:
        return f'{self.school.name}: {self.roll_number}'


class Post(models.Model):
    title = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='title', unique=True)
    content = models.TextField()
    date_posted = models.DateTimeField(default=timezone.now)
    school = models.ForeignKey(School,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.school.user.name}: {self.title}' 
    
    def get_absolute_url(self):
        return reverse('post-create')
    
#School
##slug
##scho0l_name
##state
##city
##email
##school_url

###
#student/school
#name
#username
#password
#con-password

#CHild
##slug
##child_name
##roll_num
##school_name
##parent_email
##parent_mobile_num

#name
#phone_num
#email