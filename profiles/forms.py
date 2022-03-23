from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import User, School, Student



class StudentSignUpForm(UserCreationForm):
    phone_number = forms.CharField(required=True)
    email = forms.EmailField(required=True) 
    roll_number = forms.CharField(required=True)
    school = forms.ModelChoiceField(queryset=School.objects.all(), )

    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self):
        user = User.objects.filter(username=self.request.user.username)[0]
        user.phone_number = self.cleaned_data.get('phone_number')
        user.email = self.cleaned_data.get('email')
        user.save()  
        student = Student.objects.create(user=user)
        student.roll_number = self.cleaned_data.get('roll_number')
        student.school = self.cleaned_data.get('school')
        student.save()
        return user