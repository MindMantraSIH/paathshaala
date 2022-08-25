from django.urls import path
from . import views

urlpatterns = [
    path("hi/", views.happiness_index , name="HappinessIndex"),
    path('dashboard/',views.dashboard ,name='Dashboard'),
    path('index/',views.happiness_index ,name='happiness'),
    path('upload/',views.upload_csv ,name='csv'),
    path('sendforms/',views.send ,name='send'),
    path("standard/<int:std>/", views.standard_analytics, name="standard"),
    path('student-dashboard',views.student_dashboard,name='Student-Dashboard'),
    # path("discussion/<int:myid>/", views.replies, name="replies")
    # path('', views.dashboard1, name="dashboard"),
    ]