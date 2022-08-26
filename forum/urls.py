from django.urls import path
from . import views
# app_name = 'forum'
urlpatterns = [
    path("", views.forum, name="forum"),
    path("add_post", views.add_post, name="forum_add_post"),
    path("post/<str:slug>", views.post_detail, name="forum_post_detail"),
    path("add_comment", views.add_comment, name="forum_add_comment"),
    path("delete_post", views.delete_post, name="forum_delete_post"),
    path("delete_comment", views.delete_comment, name="forum_delete_comment"),
    path("counselor-forum", views.counselor_forum, name="counselor_forum"),
    # path("discussion/<str:slug>/reply", views.replies, name="replies"),
    # path("discussion/<str:slug>/comment", views.comment, name="comment"),
    # path("discussion/<str:slug>/update", views.discussionUpdate, name="discussionUpdate"),
    # path("discussion/<str:slug>/delete", views.discussionDelete, name="discussionDelete"),
    #path("discussion/<int:pk>/", views.replyUpdate, name="replyUpdate"),

    path("base/", views.base_temp, name="base"),

]
