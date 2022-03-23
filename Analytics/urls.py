from django.urls import path
from . import views

urlpatterns = [
    path("hi/", views.happiness_index , name="HappinessIndex"),
    path('dashboard/',views.dashboard ,name='Dashboaard')
    #path("discussion/<int:myid>/", views.replies, name="replies")
    ]