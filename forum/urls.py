from django.urls import path
from . import views

urlpatterns = [
    path("", views.forum, name="forum"),
    path("discussion/<int:myid>/reply", views.replies, name="replies"),
    path("discussion/<int:myid>/comment", views.comment, name="comment"),
    path("discussion/<int:pk>/update", views.discussionUpdate, name="discussionUpdate"),
    path("discussion/<int:pk>/delete", views.discussionDelete, name="discussionDelete"),
    #path("discussion/<int:pk>/", views.replyUpdate, name="replyUpdate"),
    #path("myprofile/", views.myprofile, name="Myprofile"),
]
