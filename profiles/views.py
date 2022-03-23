from django.shortcuts import render,redirect
from .models import School,Post,Student,User
from django.contrib.auth import authenticate, login
#from .models import 

# def temp(request):
#     context={
#         'temp': .objects.all(),
#     }
#     return render(request,'profiles/temp.html',context)
from .forms import SchoolSignUpForm,StudentSignUpForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
import hashlib

class PostCreateView(CreateView):
	model = Post
	fields = ['title', 'content']

	def form_valid(self, form):
		test = School.objects.first()
		print(test)
		form.instance.school = test
		return super().form_valid(form)


# class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
# 	model = Post
# 	fields = ['title', 'content']

# 	def form_valid(self, form):
# 		form.instance.school = self.request.user.school
# 		return super().form_valid(form)

# 	def test_func(self):
# 		post = self.get_object()
# 		if self.request.user.school == post.school.user:
# 			return True
# 		return False


# class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
# 	model = Post

# 	def test_func(self):
# 		post = self.get_object()
# 		if self.request.user.school == post.school.user:
# 			return True
# 		return False

# 	success_url = '/'


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
			passw = hashlib.sha256(passw).hexdigest()
			print(passw)
			if User.objects.filter(username=username).exists():
				return render(request, 'profiles/loginregister.html', {'message': 'Username Already exists'})
			if cat == 'student':
				user = User.objects.create(username=username, name=name, password=passw, is_student=True)
				user.save()
				return redirect('student-register')
			if cat == 'school':
				user = User.objects.create(username=username, name=name, password=passw, is_school=True)
				user.save()
				return redirect('school-register')
		elif form=='sign-in':
			
			username = request.POST.get('username')
			passw = request.POST.get('password')
			user = authenticate(request, username=username, password=passw)
			print('1',user)
			if user is not None:
				print('HEYEHY')
				login(request, user)
				return redirect('home')
			print(username)
			print(passw)
			if User.objects.filter(username=username).exists():
				print('in if')
				user = User.objects.filter(username=username)[0]
				print(user)
				if user.password == passw:
					return redirect('home')
				else:
					return render(request, 'profiles/loginregister.html', {'message': 'Username or password entered is incorrect'})
			else:
				return render(request, 'profiles/loginregister.html', {'message': 'Username or password entered is incorrect'})
		

	return render(request, 'profiles/loginregister.html')

def home(request):
	if request.user.is_authenticated:
		print("User is logged in :)")
		print(f"Username --> {request.user.username}")
	else:
		print("User is not logged in :(")
	return render(request,'profiles/home.html',{'user':request.user.username})

def school_register(request):
	return render(request, 'profiles/school_register.html')

def student_register(request):
	return render(request, 'profiles/student_register.html')

