from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import smtplib

from django.conf import settings
from django.core.mail import send_mail



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
        message = f'https://www.verywellfamily.com/improve-childrens-mental-health-4154379 https://www.parents.com/health/healthy-happy-kids/why-and-how-to-teach-kids-mindfulness/ https://kidshelpphone.ca/get-info/how-practice-self-care/ https://www.mhanational.org/what-every-child-needs-good-mental-health' 
        email_from = settings.EMAIL_HOST_USER
        recipient_list = ['jobhunt2511@gmail.com']
        send_mail( subject, message, email_from, recipient_list )
        return redirect('getdata')
    return render(request, 'selfasses.html')