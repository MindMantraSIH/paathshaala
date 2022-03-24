from django.shortcuts import render
from .models import Councellor

# Create your views here.
def counsellor(request):
    if request.method == "POST":
        email = request.POST.get('email')
        address = request.POST.get('address')
        problem = request.POST.get('problem')
        c = Councellor.objects.create(email=email,address=address,problem=problem)
    return render(request, 'counsellor/councellor_connect.html')