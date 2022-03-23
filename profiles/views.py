from django.shortcuts import render,redirect
from .models import School,Student,User
from django.contrib.auth import authenticate, login, logout
#from .models import 

# def temp(request):
#     context={
#         'temp': .objects.all(),
#     }
#     return render(request,'profiles/temp.html',context)
from .forms import StudentSignUpForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
import hashlib

# class PostCreateView(CreateView):
# 	model = Post
# 	fields = ['title', 'content']

# 	def form_valid(self, form):
# 		test = School.objects.first()
# 		print(test)
# 		form.instance.school = test
# 		return super().form_valid(form)

def home(request):
	return render(request, 'profiles/home.html')


def school_register(request):
	if request.method == 'POST':
		form = SchoolSignUpForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, f'Your account has been created! You are now able to log in')
			return redirect('school-login')
	else:
		form = SchoolSignUpForm()
	return render(request, 'profiles/school_register.html', {'form': form})

def student_register(request):
	if request.method == 'POST':
		form = StudentSignUpForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, f'Your account has been created! You are now able to log in')
			return redirect('student-login')
	else:
		form = StudentSignUpForm()
	return render(request, 'profiles/student_register.html', {'form': form})


def loginregister(request):
	context = {}
	logout(request)
	if request.method == 'POST':
		form = request.POST.get('type')
		if form=='register':
			cat = request.POST.get('category')
			username = request.POST.get('username')
			name = request.POST.get('name')
			passw = request.POST.get('password')
			cpassw = request.POST.get('con_password')
			if passw != cpassw:
				return render(request, 'profiles/loginregister.html', {'message': 'Password Doesnt Match'})
			if User.objects.filter(username=username).exists():
				return render(request, 'profiles/loginregister.html', {'message': 'Username Already exists'})
			if cat == 'student':
				user = User.objects.create(username=username, name=name, is_student=True)
				user.set_password(passw)
				user.save()
				user = authenticate(request, username=username, password = passw)
				login(request,user)
				return redirect('student-register')
			if cat == 'school':
				user = User.objects.create(username=username, name=name, is_school=True)
				user.set_password(passw)
				user.save()
				user = authenticate(request, username=username, password = passw)
				login(request,user)
				return redirect('school-register')
		elif form=='sign-in':
			username = request.POST.get('username')
			passw = request.POST.get('password')
			user = authenticate(request, username=username, password=passw)
			if user is not None:
				login(request,user)
				return redirect('home')

		

	return render(request, 'profiles/loginregister.html')

def home(request):
	if request.user.is_authenticated:
		print("User is logged in :)")
		print(f"Username --> {request.user.username}")
	else:
		print("User is not logged in :(")
	return render(request,'profiles/home.html',{'user':request.user})

def school_register(request):
	print(request.user.username)
	if request.method == 'POST':
		board = request.POST.get('board')
		phone_num = request.POST.get('pno')
		email = request.POST.get('email')
		address = request.POST.get('address')
		state = request.POST.get('state')
		city = request.POST.get('city')
		user = User.objects.filter(username=request.user.username)[0]
		user.email = email
		user.phone_number = phone_num
		school = School.objects.create(user=user)
		school.board = board
		school.address = address
		school.city = city
		school.state = state
		school.save()
		user.save()
		return redirect('school-feed',slug=user.slug)

	return render(request, 'profiles/school_register.html')

def student_register(request):
	if request.method == 'POST':
		form = StudentSignUpForm(request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, f'Your account has been created! You are now able to log in')
			return redirect('student-login')
	else:
		form = StudentSignUpForm()
	return render(request, 'profiles/student_register.html', {'form': form})


