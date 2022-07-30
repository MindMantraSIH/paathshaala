from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import smtplib
import json
import urllib
import requests
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
        #suggest councellors
        where = urllib.parse.quote_plus("""
        {
            "postalCode": {
                "$exists": true
            }
        }
        """)
        url = 'https://parseapi.back4app.com/classes/Indiapincode_Dataset_India_Pin_Code?limit=10&where=%s' % where
        headers = {
            'X-Parse-Application-Id': 'bHlRdsQW7pcr9PsKHkCgACWO1REdEOxrAwh1WSZY', # This is your app's application id
            'X-Parse-REST-API-Key': 'e4CDU4Y70vtx3aUxqabHOI8ia5Q1c9jnXfc1iarx' # This is your app's REST API key
        }
        data = json.loads(requests.get(url, headers=headers).content.decode('utf-8')) # Here you have the data that you need
        print(json.dumps(data, indent=2))

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
    return render(request, 'selfasses.html')