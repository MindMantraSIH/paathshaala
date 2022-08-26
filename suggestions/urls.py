from django.urls import path
from . import views
from django.urls import path, include

urlpatterns = [
    path('',views.savedata,name="savedata"),
    path('feedback/', views.feedback, name="feedback"),
    path('feedback1/', views.feedback1, name="feedback1"),
    path('video',views.show_video, name='video_show')
 
]
