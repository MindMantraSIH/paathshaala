from django.shortcuts import render,redirect
#from .models import 

# def temp(request):
#     context={
#         'temp': .objects.all(),
#     }
#     return render(request,'profiles/temp.html',context)
from .forms import UserRegisterForm


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            return redirect('')
    else:
        form = UserRegisterForm()
    return render(request, 'profiles/register.html', {'form': form})