from django.contrib import admin
from .models import School, Student, User, Counselor
from django.core.mail import send_mail
from django.template.loader import render_to_string

admin.site.register(School)
admin.site.register(Student)
admin.site.register(User)



class CounselorAdmin(admin.ModelAdmin):
	list_display = ("user","speciality",'pincode',"is_active",)
	search_fields = ['user__name','speciality','pincode',"is_active"]
	actions = ['activate_counselor']

	def activate_counselor(self, request, queryset):
		msg_plain = render_to_string('profiles/email.txt')
		for query in queryset:
			send_mail(
				'Activation',
				msg_plain,
				'mindmantrasih@gmail.com', #sender
				[query.user.email],
				html_message=render_to_string('profiles/email.html', {'name': query.user.name}),
			)
			query.is_active = True
			query.save()
admin.site.register(Counselor, CounselorAdmin)