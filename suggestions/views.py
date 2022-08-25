from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import *

def savedata(request):
    print("saving")
    if request.method=="POST":
        print("hello")
        school = request.user.student.school
        std = request.POST.get('std')
        # print(request.user.student.school)
        levelc = request.POST.get('levelc')
        print(levelc)
        env = request.POST.get('env')
        teachersc = request.POST.get('teachersc')
        prevdisc = request.POST.get('prevdisc')
        fecilities = request.POST.get('fecilities')
        timetable = request.POST.get('timetable')
        grpwork = request.POST.get('grpwork')
        mentalhlth = request.POST.get('mentalhlth')
        sportart = request.POST.get('sportart')
        solveprob = request.POST.get('solveprob')
        creativecourse = request.POST.get('creativecourse')
        foconindv = request.POST.get('foconindv')
        mannlearn = request.POST.get('mannlearn')
        courserele = request.POST.get('courserele')
        issuesofconc = request.POST.get('issuesofconc')
        aresolved = request.POST.get('aresolved')
        others = request.POST.get('others')
        data = Data(school=school, std= std,levelc=levelc,
                    env=env,teachersc=teachersc,prevdisc=prevdisc,
                    fecilities=fecilities,timetable=timetable,
                    grpwork=grpwork,mentalhlth=mentalhlth,
                    sportart=sportart,solveprob=solveprob,
                    creativecourse=creativecourse,foconindv=foconindv,
                    mannlearn=mannlearn,courserele=courserele,
                    issuesofconc=issuesofconc,aresolved=aresolved,others=others)

        data.save()
        print("done")
        return redirect('home')
    return render(request,'sugg.html')
        