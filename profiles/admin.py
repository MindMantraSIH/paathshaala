from django.contrib import admin
from .models import School, Student, User, Post

admin.site.register(School)
admin.site.register(Student)
admin.site.register(User)
admin.site.register(Post)