from django import forms
# from django.contrib.auth.forms import UserUpdate
from django.db import transaction
from .models import User, School, Student



class StudentSignUpForm(forms.ModelForm):
    phone_number = forms.CharField(required=True)
    email = forms.EmailField(required=True) 
    roll_number = forms.CharField(required=True)
    school = forms.ModelChoiceField(queryset=School.objects.all())

    class Meta:
        model = User
        fields = ('phone_number', 'email')

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super(StudentSignUpForm, self).__init__(*args, **kwargs)

    @transaction.atomic
    def save(self):
        user = User.objects.filter(username=self.user.username)[0]
        user.phone_number = self.cleaned_data.get('phone_number')
        user.email = self.cleaned_data.get('email')
        # student = Student.objects.create(user=user)
        student = Student()
        student.user = user
        student.roll_number = self.cleaned_data.get('roll_number')
        student.school = self.cleaned_data.get('school')
        student.save()
        user.save()  
        return user