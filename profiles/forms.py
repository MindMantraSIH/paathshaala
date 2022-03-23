from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import User, School, Student


class SchoolSignUpForm(UserCreationForm):
    phone_number = forms.CharField(required=True)
    email = forms.EmailField(required=True) 
    state = forms.CharField(required=True) 
    city = forms.CharField(required=True)
    name = forms.CharField(required=True)
    school_url = forms.URLField(required=False)

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_school = True
        user.name = self.cleaned_data.get('name')
        user.phone_number = self.cleaned_data.get('phone_number')
        user.email = self.cleaned_data.get('email')
        user.save()  
        school = School.objects.create(user=user)
        school.state = self.cleaned_data.get('state')
        school.city = self.cleaned_data.get('city')
        school.school_url = self.cleaned_data.get('school_url')
        school.save()
        return user

class StudentSignUpForm(UserCreationForm):
    phone_number = forms.CharField(required=True)
    email = forms.EmailField(required=True) 
    name = forms.CharField(required=True)
    roll_number = forms.CharField(required=True)
    school = forms.ModelChoiceField(queryset=School.objects.all(), )

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.is_student = True
        user.name = self.cleaned_data.get('name')
        user.phone_number = self.cleaned_data.get('phone_number')
        user.email = self.cleaned_data.get('email')
        user.save()  
        student = Student.objects.create(user=user)
        student.roll_number = self.cleaned_data.get('roll_number')
        student.school = self.cleaned_data.get('school')
        student.save()
        return user