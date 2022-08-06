from django.shortcuts import render,redirect
from .models import School,Student,User, Counsellor
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

def home(request):
	return render(request,'profiles/home.html')

def student_register(request):
	if request.method == 'POST':
		form = StudentSignUpForm(request.user, request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, f'Your account has been created! You are now able to log in')
			return redirect('school-feed', request.user.student.school.user.slug)
	else:
		form = StudentSignUpForm(request.user)
	return render(request, 'profiles/student_register.html', {'form': form})


def loginregister(request):
	logout(request)
	if request.method == 'POST':
		form = request.POST.get('type')
		print(form)
		if form=='register':
			cat = request.POST.get('category')
			print(cat)
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
				print(user)
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
				if user.is_school:
					return redirect('school-feed', user.slug)
				else:
					return redirect('school-feed',user.student.school.user.slug)
			else:
				return render(request, 'profiles/loginregister.html', {'message': 'Username or password is incorrect'})

		

	return render(request, 'profiles/loginregister.html')

def home(request):
	if request.user.is_authenticated:
		print("User is logged in :)")
		print(f"Username --> {request.user.username}")
	else:
		print("User is not logged in :(")
	return render(request,'profiles/home.html',{'user':request.user})

def school_register(request):
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
def counselor_register(request):
	if request.method == 'POST':
		email = request.POST.get('email','')
		phone_num = request.POST.get('phone_no',"")
		description = request.POST.get('description',"")
		address = request.POST.get('address',"")
		pincode = request.POST.get('pincode',"")
		speciality = request.POST.get('speciality',"")
		awards = request.POST.get('awards',"")
		fees = request.POST.get('fees',"")
		id_proof = request.FILES['id_proof']
		user = User.objects.get(username=request.user.username)
		user.email = email
		user.phone_number = phone_num
		counsellor = Counsellor.objects.create(user=user)
		counsellor.description = description
		counsellor.address = address
		counsellor.pincode = pincode
		counsellor.speciality = speciality
		counsellor.awards = awards
		counsellor.fees = fees
		counsellor.medical_id_proof = id_proof
		counsellor.save()
		user.save()
		return redirect('awaiting-confirmation')
	
	return render(request, 'profiles/counsellor_register.html')
def logout_view(request):
	logout(request)
	return redirect('home')
