from django.urls import path
from . import views

urlpatterns = [
    path("", views.forum, name="Forum"),
    path("discussion/<int:myid>/", views.replies, name="replies"),
    path("discussion/<int:pk>/update", views.discussionUpdate, name="discussionUpdate"),
    path("discussion/<int:pk>/delete", views.discussionDelete, name="discussionDelete"),
    path("discussion/<int:pk>/", views.replyUpdate, name="replyUpdate"),
    #path("myprofile/", views.myprofile, name="Myprofile"),
]
