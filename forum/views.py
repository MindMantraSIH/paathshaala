from http.client import HTTPResponse
from uuid import RESERVED_FUTURE
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required

from profiles.models import Counselor
from .models import Profile, Discussion, Reply, ForumPost, ForumComments
from .forms import *
from huggingface_hub.inference_api import InferenceApi
from django.http import JsonResponse

#from django.contrib.auth.models import User
from django.conf import settings
#User = settings.AUTH_USER_MODEL



def post_detail(request, slug=''):
    post = ForumPost.objects.get(slug=slug)
    comments = ForumComments.objects.filter(post = post).order_by('-timestamp')
    comments_count = comments.count()
    return render(request, "forum/forum_post_detail.html", locals())

@login_required
def forum(request):
    posts = ForumPost.objects.all().order_by('-timestamp')
    return render(request, "forum/forum.html", {'posts':posts})

@login_required
def add_post(request):
    if request.method=="POST":
        try:
            post_id = request.POST.get('post_id')
            post = ForumPost.objects.get(id = post_id)
            is_update = True
        except:
            is_update = False
            post = ForumPost()
        print(request.POST)   
        content = request.POST.get('content')
        title = request.POST.get('title')
        inference = InferenceApi("bhadresh-savani/distilbert-base-uncased-emotion")
        infer = inference(inputs=content)[0][0]['label']
        infer_all = inference(inputs=content)[0]
        print(infer)
        print(infer_all)
        is_flagged = False
        if infer in ["sadness","fear","anger"]:
            is_flagged=True
        print('POSTTT')
        print(content,title)
        post.content = content
        post.title = title
        post.user = request.user
        post.is_flagged = is_flagged
        post.save()
        #return render(request, "forum.html")
    if is_update:
        return JsonResponse({'message':'success'})
    posts = ForumPost.objects.all().order_by('-timestamp')
    return render(request, "forum/forum_posts.html", locals())

@login_required
def add_comment(request):
    post_id = ''
    if request.method=="POST":  
        comment = request.POST.get('comment')
        post_id = request.POST.get('post_id')
        post_comment = ForumComments()
        post_comment.content = comment
        post_comment.user = request.user
        post = ForumPost.objects.get(id = post_id)
        post_comment.post = post
        post_comment.save()
    comments = ForumComments.objects.filter(post = post).order_by('-timestamp')
    comments_count = comments.count()
    return render(request, "forum/forum_post_comments.html", locals())

@login_required
def delete_post(request):
    if request.method == "POST":
        post_id = request.POST.get('post_id')
        post = ForumPost.objects.get(id = post_id)
        post.delete()
    return JsonResponse({'message':'success'})

@login_required
def delete_comment(request):
    if request.method == "POST":
        comment_id = request.POST.get('comment_id')
        comment = ForumComments.objects.get(id = comment_id)
        post = comment.post
        comment.delete()
    comments = ForumComments.objects.filter(post = post).order_by('-timestamp')
    comments_count = comments.count()
    return render(request, "forum/forum_post_comments.html", locals())

@login_required
def counselor_forum(request):
    if request.user.is_counselor:
        counselor_obj = Counselor.objects.get(user = request.user)
        print('hdfs')
        if counselor_obj.is_active:
            print('here')
            posts = ForumPost.objects.filter(is_flagged=True).order_by('-timestamp')
            return render(request, "forum/forum.html", {'posts':posts})
        else:
            return redirect("awaiting-confirmation")
    else:
        return JsonResponse({"message":'Not Allowed'})


def base_temp(request):
    return render(request, 'forum/base-temp.html')
    