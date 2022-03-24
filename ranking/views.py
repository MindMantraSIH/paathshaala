from django.shortcuts import render
from profiles.models import School
def schoolinfo(request):
    school=School.objects.order_by('rank')
    context={
        'school':school,
    }
    return render(request,'ranking/Ranking.html',context)