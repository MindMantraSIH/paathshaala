from django.urls import path
from . import views

urlpatterns = [
    path("", views.forum, name="forum"),
    path("comments/", views.forum_extended, name="forum-extended")
    # path("discussion/<str:slug>/reply", views.replies, name="replies"),
    # path("discussion/<str:slug>/comment", views.comment, name="comment"),
    # path("discussion/<str:slug>/update", views.discussionUpdate, name="discussionUpdate"),
    # path("discussion/<str:slug>/delete", views.discussionDelete, name="discussionDelete"),
    #path("discussion/<int:pk>/", views.replyUpdate, name="replyUpdate"),
    #path("myprofile/", views.myprofile, name="Myprofile"),
]
