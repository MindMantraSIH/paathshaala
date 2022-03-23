from django.contrib import admin

from .models import Discussion, Reply, Profile

admin.site.register(Profile)
admin.site.register(Discussion)
admin.site.register(Reply)