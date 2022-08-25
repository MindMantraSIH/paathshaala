from django.urls import path
from . import views

urlpatterns = [
    path("", views.ques, name="criticalthinkingques"),
    path("add_post", views.add_post, name="add_post"),
    path("post/<str:slug>", views.post_detail, name="post_detail"),
    path("add_comment", views.add_comment, name="add_comment"),
    path("delete_post", views.delete_post, name="delete_post"),
    path("delete_comment", views.delete_comment, name="delete_comment"),

]
