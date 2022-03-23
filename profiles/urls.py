from django.urls import path
from . import views

urlpatterns = [
    #path('temp', views.temp , name='temp'),
    path('register/', views.register , name='register'),
]
