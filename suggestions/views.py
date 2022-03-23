from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import *

def savedata(request):
    if request.method=="POST":
        data = Data(request.POST)
        if data.is_valid():
            data.save()
            return redirect('')
    return render(request,'sugg.html')
        