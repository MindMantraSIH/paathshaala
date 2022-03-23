from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import smtplib


@login_required()
def getdata(request):
    if request.method == 'POST':
        ans = request.POST.getlist('ans[]')
        sender = 'jobhunt2511@gmail.com'
        receivers = ['jobhunt2511@gmail.com']
        message = """From: From Person <jobhunt2511@gmail.com>
        To: To Person <jobhunt2511@gmail.com>
        Subject: SMTP e-mail test

        This is a test e-mail message.
        """
        try:
            smtpObj = smtplib.SMTP('localhost')
            smtpObj.sendmail(sender, receivers, message)
            print("Successfully sent email")
        except smtplib.SMTPException:
            print("Error: unable to send email")
        return redirect('')
    return render(request, 'selfasses.html', {'ans':ans})