from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import *
from django.http import JsonResponse
from django.conf import settings

def post_detail(request, slug=''):
    post = quesPost.objects.get(slug=slug)
    comments = quesComments.objects.filter(post = post).order_by('-timestamp')
    comments_count = comments.count()
    return render(request, "criticalthinkingquestions/ques_post_detail.html", locals())

@login_required
def ques(request):
    posts = quesPost.objects.all().order_by('-timestamp')
    return render(request, "criticalthinkingquestions/ques.html", {'posts':posts})

@login_required
def add_post(request):
    if request.method=="POST":
        try:
            post_id = request.POST.get('post_id')
            post = quesPost.objects.get(id = post_id)
            is_update = True
        except:
            is_update = False
            post = quesPost()
        print(request.POST)           
        title = request.POST.get('title')
        
        print(title)
        post.title = title
        post.user = request.user
        post.save()

    if is_update:
        return JsonResponse({'message':'success'})
    posts = quesPost.objects.all().order_by('-timestamp')
    return render(request, "criticalthinkingquestions/ques_posts.html", locals())

@login_required
def add_comment(request):
    post_id = ''
    if request.method=="POST":  
        comment = request.POST.get('comment')
        post_id = request.POST.get('post_id')
        post_comment = quesComments()
        post_comment.content = comment
        post_comment.user = request.user
        post = quesPost.objects.get(id = post_id)
        post_comment.post = post
        post_comment.save()
    comments = quesComments.objects.filter(post = post).order_by('-timestamp')
    comments_count = comments.count()
    return render(request, "criticalthinkingquestions/ques_post_comments.html", locals())

@login_required
def delete_post(request):
    if request.method == "POST":
        post_id = request.POST.get('post_id')
        post = quesPost.objects.get(id = post_id)
        post.delete()
    return JsonResponse({'message':'success'})

@login_required
def delete_comment(request):
    if request.method == "POST":
        comment_id = request.POST.get('comment_id')
        comment = quesComments.objects.get(id = comment_id)
        post = comment.post
        comment.delete()
    comments = quesComments.objects.filter(post = post).order_by('-timestamp')
    comments_count = comments.count()
    return render(request, "criticalthinkingquestions/ques_post_comments.html", locals())




@login_required
def brainstormDelete(request,slug):
    disc=Brainstorm.objects.get(slug=slug)
    disc.delete()
    posts = Brainstorm.objects.all()
            #print(posts)
    return redirect('criticalthinkingquestions')