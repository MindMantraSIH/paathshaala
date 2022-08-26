from django.urls import path
from . import views
from django.urls import path, include

urlpatterns = [
    path('',views.savedata,name="savedata"),
    path('video',views.show_video, name='video_show')
]
