from django.urls import path
from . import views

urlpatterns = [
    #path('temp', views.temp , name='temp'),
    # path("new-post/",  views.PostCreateView.as_view(), name='post-create'),
    path('school-register/',views.school_register,name="school-register"),
    path('student-register/',views.student_register,name="student-register"),
    path('loginregister/',views.loginregister,name="loginregister"),
    path('home/',views.home,name="home"),
    path('school-login/',views.school_register,name="school-login"),
    path('student-login/',views.student_register,name="student-login"),
    path('school-home/',views.schoolhome,name="schoolhome"),
]
