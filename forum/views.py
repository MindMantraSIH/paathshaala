from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import Profile, Discussion, Reply
from .forms import *

#from django.contrib.auth.models import User
from django.conf import settings
#User = settings.AUTH_USER_MODEL



@login_required
def forum(request):
    profile = Profile.objects.all()
    if request.method=="POST":   
        user = request.user
        content = request.POST.get('content')
        title = request.POST.get('title')
        post = Discussion(user1=user, disc_title=title,disc_content=content)
        post.save()
        print("hello")
        #return render(request, "forum.html")
    posts = Discussion.objects.all()
    print(posts)
    return render(request, "forum.html", {'posts':posts})

#@login_required(login_url = '/login')
@login_required
def replies(request, myid):
    post = Discussion.objects.filter(id=myid).first()
    replies = Reply.objects.filter(post=post)
    if request.method=="POST":
        user = request.user
        desc = request.POST.get('desc')
        post_id =request.POST.get('post_id')
        reply = Reply(user = user, reply_content = desc, post=post)
        reply.save()
        print(reply)
        #return render(request, "forum.html")
    return render(request, "forum.html", {'post':post})


@login_required
def discussionUpdate(request,pk):
    disc=Discussion.objects.get(id=pk)
    print(disc)
    #user = User.objects.get(id = request.user.id)
    #print(user)
    if request.method == 'POST':
        upd_form = DiscussionUpdateForm(request.POST)
        if upd_form.is_valid():
            a=upd_form.save(commit=False)
            a.id=pk
            a.save()
            print(type(upd_form))
            #user.profile= request.user.profile
            posts = Discussion.objects.all()
            #print(posts)
            return render(request, "forum.html", {'posts':posts})

    else:
        upd_form = DiscussionUpdateForm(instance=request.user)

    context = {
        'upd_form': upd_form
    }

    return render(request, 'DiscussionUpdate.html', context)


@login_required
def replyUpdate(request):
    user = User.objects.get(id = request.user.id)
    #print(user)
    if request.method == 'POST':
        upd_form = ReplyUpdateForm(request.POST,instance=request.user)
        if upd_form.is_valid():
            upd_form.save()
            #user.profile= request.user.profile
            return redirect('')

    else:
        upd_form = ReplyUpdateForm(instance=request.user)

    context = {
        'upd_form': upd_form
    }

    return render(request, 'ReplyUpdate.html', context)

@login_required
def discussionDelete(request,pk):
    disc=Discussion.objects.get(id=pk)
    disc.delete()
    posts = Discussion.objects.all()
            #print(posts)
    return render(request, "forum.html", {'posts':posts})

