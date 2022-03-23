from django.db import models
from django.contrib.auth.models import User
#from autoslug import AutoSlugField
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    is_school = models.BooleanField('school status',default=False)
    is_student = models.BooleanField('student status',default=False)
    name = models.CharField(max_length=100)
    #slug = AutoSlugField(populate_from='name')
    phone_num = models.CharField(max_length=10)
    email = models.EmailField()

class School(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    school_url = models.URLField(null=True,blank=True)


    def __str__(self) -> str:
        return self.user.name

class Student(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    roll_number = models.CharField(max_length=20)
    school = models.ForeignKey(School, on_delete=models.CASCADE)
    

    def __str__(self) -> str:
        return f'{self.school.name}: {self.roll_number}'
    
#School
##slug
##scho0l_name
##state
##city
##email
##school_url


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