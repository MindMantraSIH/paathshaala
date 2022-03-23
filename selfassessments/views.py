from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import smtplib

from django.conf import settings
from django.core.mail import send_mail


@login_required()
def getdata(request):
    print(request.method)
    if request.method == 'POST':
        for i in request.POST:
            print(i)
        ans = request.POST.getlist('ans[]')
        print(ans,"list")
        subject = 'test'
        message = f'Hi'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['jobhunt2511@gmail.com']
        send_mail( subject, message, email_from, recipient_list )
        return redirect('getdata')
    return render(request, 'selfasses.html')