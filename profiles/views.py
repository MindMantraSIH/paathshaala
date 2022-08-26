from django.shortcuts import render,redirect
from .models import Counselor, School,Student,User
from django.contrib.auth import authenticate, login, logout
#from .models import 
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
import hashlib
from Analytics.populate_database import create_student_data_csv, database_happiness_index_survey
import json
import urllib
import requests

def home(request):
	return render(request,'profiles/home.html')

def student_register(request):
	print('HEHU')
	if request.method == 'POST':
		user = User.objects.get(id = request.user.id)
		user.phone_number = request.POST.get('pno','')
		user.email = request.POST.get('email','')
		user.is_student = True
		student = Student()
		student.user = user
		student.roll_number = request.POST.get('rollno','')
		school = request.POST.get('schoolname','')
		print(school)
		student.school = School.objects.get(user_id=school)
		student.pincode = request.POST.get('pincode','')
		user.std = request.POST.get('standard','')
		user.division = request.POST.get('division','')
		student.save()
		user.save()  
		messages.success(request, f'Your account has been created! You are now able to log in')
		return redirect('school-feed', request.user.student.school.user.slug)
	schools = School.objects.all()
	return render(request, 'profiles/student_register.html', locals())


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
				user = User.objects.create(username=username, name=name)
				print(user)
				user.set_password(passw)
				user.save()
				user = authenticate(request, username=username, password = passw)
				login(request,user)
				return redirect('student-register')
			elif cat == 'school':
				user = User.objects.create(username=username, name=name)
				user.set_password(passw)
				user.save()
				user = authenticate(request, username=username, password = passw)
				login(request,user)
				return redirect('school-register')
			elif cat == 'counselor':
				user = User.objects.create(username=username, name=name)
				user.set_password(passw)
				user.save()
				user = authenticate(request, username=username, password = passw)
				login(request,user)
				return redirect('counselor-register')
		elif form=='sign-in':
			username = request.POST.get('username')
			passw = request.POST.get('password')
			user = authenticate(request, username=username, password=passw)
			if user is not None:
				login(request,user)
				if user.is_school:
					return redirect('school-feed', user.slug)
				elif user.is_student:
					return redirect('school-feed',user.student.school.user.slug)
				else:
					return redirect('counselor_forum')
			else:
				return render(request, 'profiles/loginregister.html', {'message': 'Username or password is incorrect'})

		

	return render(request, 'profiles/loginregister.html')

def home(request):
	# database_happiness_index_survey()
	# create_student_data_csv(request.user.id)
	if request.user.is_authenticated:
		print("User is logged in :)")
		print(f"Username --> {request.user.username}")
	else:
		print("User is not logged in :(")
	return render(request,'profiles/home.html',{'user':request.user})


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
		user = User.objects.get(id=request.user.id)
		user.email = email
		user.phone_number = phone_num
		user.is_counselor=True
		counselor = Counselor.objects.create(user=user)
		counselor.description = description
		counselor.address = address
		counselor.pincode = pincode
		where = urllib.parse.quote_plus("""
		{
		    "postalCode": "%s"
		}
		"""%pincode)
		url = 'https://parseapi.back4app.com/classes/Indiapincode_Dataset_India_Pin_Code?limit=10&order=geoPosition&where=%s' % where
		headers = {
			'X-Parse-Application-Id': 'XVP5z4O2TOGHKYc7LbbUCFX5Tbctw4dYw1r5zRri',  # This is your app's application id
			'X-Parse-REST-API-Key': 'uVTRFN5134RMaQzCw1YFhWn5RohmS63ryEACBrxI'  # This is your app's REST API key
		}
		data = json.loads(
			requests.get(url, headers=headers).content.decode('utf-8'))  # Here you have the data that you need


		counselor.latitude = str(data.get('results')[0].get('geoPosition').get('latitude'))
		counselor.longitude = str(data.get('results')[0].get('geoPosition').get('longitude'))
		counselor.speciality = speciality
		counselor.awards = awards
		counselor.fees = fees
		counselor.medical_id_proof = id_proof
		counselor.save()
		user.save()
		return redirect('awaiting-confirmation')
	
	return render(request, 'profiles/counsellor_register.html')

def awaiting_confirmation(request):
	return render(request, 'profiles/awaiting_confirmation.html')

def school_register(request):
	print('haaha')
	print(request.method)
	if request.method == 'POST':
		print('here')
		user = User.objects.get(id=request.user.id)
		board = request.POST.get('board')
		phone_num = request.POST.get('pno')
		email = request.POST.get('email')
		address = request.POST.get('address')
		state = request.POST.get('state')
		city = request.POST.get('city')
		user.email = email
		user.phone_number = phone_num
		user.is_school=True
		school = School.objects.create(user=user)
		school.board = board
		school.address = address
		school.city = city
		school.state = state
		school.save()
		user.save()
		return redirect('school-feed',slug=user.slug)
	return render(request, 'profiles/school_register.html')

def logout_view(request):
	logout(request)
	return redirect('home')

def nav_new(request):
	return render(request, 'profiles/nav_new.html')