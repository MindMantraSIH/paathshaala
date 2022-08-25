from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import smtplib
from django.contrib import messages
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string


def getdata(request):
    print(request.method)
    all={}
    if request.method == 'POST':
        
        email=request.POST.get("email")
        for i in ['d1','s1','an1','an2','d2','an3','ad1an4','d3','s2','s3','ad2','ad3','p1','p2','s4','d4','p3','s5']:
            ans=request.POST.get(i)
            all[i]=float(ans)
        dep = all['d1']+all['d2']+all['d3']+all['d4']
        st = all['s1']+all['s2']+all['s3']+all['s4']+all['s5']
        anx = all['an1']+all['an2']+all['an3']+all['ad1an4']
        ad = all['ad1an4']+all['ad2']+all['ad3']
        p = all['p1']+all['p2']+all['p3']
        tot = dep + st+anx+ad+p
        dep_percent=dep*100/tot
        st_percent=st*100/tot
        anx_percent=anx*100/tot
        ad_percent=ad*100/tot
        p_percent=p*100/tot
        print(all)
        dep_percent=dep*100/tot
        st_percent=st*100/tot
        anx_percent=anx*100/tot
        ad_percent=ad*100/tot
        p_percent=p*100/tot
        context={
            'dep_percent':dep_percent,'st_percent':st_percent,'anx_percent':anx_percent,'ad_percent':ad_percent,'p_percent':p_percent}
        subject = 'Self Assessment Report'
        message = "Dear User, \n" \
                  "Thank you for using our application.\n" \
                  "This is your final report based on your mental health assessment: \n" \
                  "(Check up with your doctor for an accurate assessment) \n"\
                  f"Depression: {dep_percent} % \n"\
                  f"Stress: {st_percent} % \n"\
                  f"Anxiety: {anx_percent} % \n"\
                  f"ADHD: {ad_percent} % \n"\
                  f"Pressure: {p_percent} % \n"\
                  "Here are some resources to help you understand mental health issues: \n" \
                  "https://www.verywellfamily.com/improve-childrens-mental-health-4154379\n" \
                  " https://www.parents.com/health/healthy-happy-kids/why-and-how-to-teach-kids-mindfulness/ \n" \
                  "https://kidshelpphone.ca/get-info/how-practice-self-care/ \n" \
                  "https://www.mhanational.org/what-every-child-needs-good-mental-health"
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        print(message)
        print(type(subject),type(message),type(email_from),type(recipient_list))
        send_mail(
            subject,
            message,
            'mindmantrasih@gmail.com', #sender
            recipient_list,
        )
        messages.success(request, 'The results are sent to your email.')
        return render(request,'selfassessments/results.html',context)
    return render(request, 'selfassessments/selfasses.html')