from django.shortcuts import render

def temp(request):
    context={
        'temp':temp,
    }
    return render(request,'profiles/temp.html',context)