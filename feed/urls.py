from django.urls import path
from . import views

urlpatterns = [
    #path('temp', views.temp , name='temp'),
    path('post-upvote-ajax/', views.upvote_ajax, name='post-upvote-ajax'),
    path("<slug:slug>",  views.school_feed, name='school-feed'),
    path('delete/<slug:school>/<slug:slug>', views.delete_feed_post, name='delete-feed-post'),
    
]