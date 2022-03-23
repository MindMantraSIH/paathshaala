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

@login_required
def comment(request,myid):
    profile = Profile.objects.all()
    post = Discussion.objects.filter(id=myid)
    #print(posts)
    replies = Reply.objects.filter(post=post[0])
    return render(request, "comment.html", {'reply':replies,'posts':post})

#@login_required(login_url = '/login')
@login_required
def replies(request, myid):
    post = Discussion.objects.get(id=myid)
    replies = Reply.objects.filter(post=post)
    if request.method=="POST":
        user = request.user
        print(user)
        rep = request.POST.get('reply')
        print(rep)
        post_id = myid
        print(post)
        print(post_id)
        reply = Reply(user = user)
        reply.reply_content = rep
        reply.post = post
        print(reply)
        reply.save()
        
    return redirect('forum')


@login_required
def discussionUpdate(request,pk):
    disc=Discussion.objects.get(id=pk)
    #print(disc)
    #user = User.objects.get(id = request.user.id)
    #print(user)
    disc.delete()
    print("in edit")
    if request.method == 'POST':
        user=request.user
        
        title=request.POST.get('title')
        content=request.POST.get('content')
        d = Discussion(user1=user, disc_title=title,disc_content=content)
        d.disc_content = content
        d.disc_title = title
        upd_form=d
        d.save()
        #upd_form = DiscussionUpdateForm(request.POST)
        print(upd_form.is_valid())
        
        return redirect('forum')

    context = {
        'upd_form': upd_form
    }

    return render(request, "DiscussionUpdate.html",context)


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
    return redirect('forum')

