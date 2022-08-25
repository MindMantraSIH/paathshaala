from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import *

def savedata(request):
    print("saving")
    student_obj = request.user.student
    std = student_obj.std
    if request.method=="POST":
        print("hello")
        if 1 <= std <= 4:
            school = request.user.student.school
            playtime = request.POST.get('playtime')
            extra_curr = request.POST.get('extra_curr')
            difficult = request.POST.get('difficult')
            materials = request.POST.get('materials')
            fear = request.POST.get('fear')
            environment = request.POST.get('environment')
            like_sch = request.POST.get('like_sch')
            like_friends = request.POST.get('like_friends')
            others = request.POST.get('others')
            solution = request.POST.get('solution')
            data = Data1(school=school,student=student_obj,playtime=playtime,extra_curr=extra_curr,difficult=difficult,materials=materials,fear=fear,environment=environment,like_sch=like_sch,like_friends=like_friends,others=others, solution=solution)
            data.save()
        elif 5 <= std <= 8:
            school = request.user.student.school
            levelc = request.POST.get('levelc')
            extra_curr = request.POST.get('extra_curr')
            course_rev = request.POST.get('course_rev')
            violence = request.POST.get('violence')
            teachers = request.POST.get('teachers')
            environment = request.POST.get('environment')
            grpwork = request.POST.get('grpwork')
            secure = request.POST.get('secure')
            anxiety = request.POST.get('anxiety')
            socially_active = request.POST.get('socially_active')
            others = request.POST.get('others')
            solution = request.POST.get('solution')
            data = Data2(school=school,student=student_obj,levelc=levelc,extra_curr=extra_curr,course_rev=course_rev,violence=violence,teachers=teachers,environment=environment,anxiety=anxiety,grpwork=grpwork,secure=secure,socially_active=socially_active,others=others, solution=solution)
            data.save()
        else:
            school = request.user.student.school
            levelc = request.POST.get('levelc')
            train = request.POST.get('train')
            exam = request.POST.get('exam')
            alhours = request.POST.get('alhours')
            support = request.POST.get('support')
            anxiety = request.POST.get('anxiety')
            alienated = request.POST.get('alienated')
            fam_burd = request.POST.get('fam_burd')
            insecure = request.POST.get('insecure')
            manner = request.POST.get('manner')
            others = request.POST.get('others')
            solution = request.POST.get('solution')
            data = Data3(school=school,student=student_obj,levelc=levelc,life_skills=train,exam_in_acc_course=exam,innovation_time=alhours,support=support,alienated=alienated,anxiety=anxiety,family_burden=fam_burd,insecurity=insecure,fundamental_rules=manner,others=others,solution=solution)
            data.save()
            print("done")
            return redirect('home')
    
    if 1 <= int(std) <= 4:
        return render(request,'suggestion_group1.html') 
    elif 5 <= int(std) <= 8:
        return render(request,'suggestion_group2.html') 
    else:
        return render(request,'suggestion_group3.html') 
        