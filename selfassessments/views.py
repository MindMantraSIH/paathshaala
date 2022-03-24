from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import smtplib

from django.conf import settings
from django.core.mail import send_mail


@login_required()
def getdata(request):
    print(request.method)
    all=[]
    if request.method == 'POST':
        print(request.POST.get("gen"))
        for i in ['std','gen','hob','act','edu','inc','extra','play','sleep','comp','prep','sport','anx','secure','conf','soc','add']:
            ans=request.POST.get(i)
            all.append(ans)
        print(all)
        subject = 'test'
        message = f'Hi'
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['jobhunt2511@gmail.com']
        send_mail( subject, message, email_from, recipient_list )
        return redirect('getdata')
    return render(request, 'selfasses.html')