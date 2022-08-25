from django.urls import path
from . import views

urlpatterns = [
    path('', views.schoolinfo , name='schoolinfo'),
    path('councel/', views.councel_rank , name='councelinfo'),
]
