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
        for i in ['std','gen','hob','act','edu','inc','extra','play','sleep','comp','prep','sport','anx','secure','conf','soc','add','email']:
            ans=request.POST.get(i)
            all.append(ans)
        print(all)
        subject = 'Self Assessment Report'
        message = "Dear User, \n" \
                  "Thank you for using our application. Here are some resources to help you based on the assessment: \n" \
                  "https://www.verywellfamily.com/improve-childrens-mental-health-4154379\n" \
                  " https://www.parents.com/health/healthy-happy-kids/why-and-how-to-teach-kids-mindfulness/ \n" \
                  "https://kidshelpphone.ca/get-info/how-practice-self-care/ \n" \
                  "https://www.mhanational.org/what-every-child-needs-good-mental-health"
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [all[-1]]
        send_mail( subject, message, email_from, recipient_list )
        return redirect('getdata')
    return render(request, 'selfassessments/selfasses.html')