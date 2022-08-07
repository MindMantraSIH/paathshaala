from django.contrib import admin

from .models import ForumPost, ForumComments

admin.site.register(ForumPost)
admin.site.register(ForumComments)