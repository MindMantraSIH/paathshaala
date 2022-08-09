from django.urls import path
from . import views
# app_name = 'forum'
urlpatterns = [
    path("", views.forum, name="forum"),
    path("add_post", views.add_post, name="add_post"),
    path("post/<str:slug>", views.post_detail, name="post_detail"),
    path("add_comment", views.add_comment, name="add_comment"),
    path("delete_post", views.delete_post, name="delete_post"),
    path("delete_comment", views.delete_comment, name="delete_comment"),
    # path("discussion/<str:slug>/reply", views.replies, name="replies"),
    # path("discussion/<str:slug>/comment", views.comment, name="comment"),
    # path("discussion/<str:slug>/update", views.discussionUpdate, name="discussionUpdate"),
    # path("discussion/<str:slug>/delete", views.discussionDelete, name="discussionDelete"),
    #path("discussion/<int:pk>/", views.replyUpdate, name="replyUpdate"),
    #path("myprofile/", views.myprofile, name="Myprofile"),
]
