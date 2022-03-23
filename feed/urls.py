from django.urls import path
from . import views

urlpatterns = [
    #path('temp', views.temp , name='temp'),
    path("<slug:slug>",  views.school_feed, name='school-feed'),
    
]