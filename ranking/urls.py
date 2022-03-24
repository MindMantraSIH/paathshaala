from django.urls import path
from . import views

urlpatterns = [
    path('', views.schoolinfo , name='schoolinfo'),
]