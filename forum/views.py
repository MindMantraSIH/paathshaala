from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
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


# @login_required
# def comment(request,slug):
#     #profile = Profile.objects.all()
#     post = Discussion.objects.filter(slug=slug)
#     #print(posts)
#     replies = Reply.objects.filter(post=post[0])
#     return render(request, "forum/comment.html", {'reply':replies,'posts':post})

# #@login_required(login_url = '/login')
# @login_required
# def replies(request, slug):
#     post = Discussion.objects.get(slug=slug)
#     replies = Reply.objects.filter(post=post)
#     if request.method=="POST":
#         user = request.user
#         print(user)
#         rep = request.POST.get('reply')
#         print(rep)
#         #post_id = myid
#         #print(post)
#         #print(post_id)
#         reply = Reply(user = user)
#         reply.reply_content = rep
#         reply.post = post
#         print(reply)
#         reply.save()
        
#     return redirect('forum')


# @login_required
# def discussionUpdate(request,slug):
#     #print(slug)
#     print("in update",Discussion.objects.all())
#     disc=Discussion.objects.get(slug=slug)
#     print(disc)
#     #print(disc)
#     #user = User.objects.get(id = request.user.id)
#     #print(user)
    
#     print("in edit")
#     if request.method == 'POST':
#         user=request.user        
#         title=request.POST.get('title')
#         content=request.POST.get('content')
#         d = Discussion(user1=user, disc_title=title,disc_content=content)
#         d.disc_content = content
#         d.disc_title = title
#         upd_form=d
#         d.save()
#         disc.delete()
#         return redirect('forum')

    

    # return render(request, "forum/DiscussionUpdate.html")


# @login_required
# def replyUpdate(request):
#     #user = User.objects.get(id = request.user.id)
#     #print(user)
#     if request.method == 'POST':
#         upd_form = ReplyUpdateForm(request.POST,instance=request.user)
#         if upd_form.is_valid():
#             upd_form.save()
#             #user.profile= request.user.profile
#             return redirect('')

#     else:
#         upd_form = ReplyUpdateForm(instance=request.user)

#     context = {
#         'upd_form': upd_form
#     }

#     return render(request, 'forum/ReplyUpdate.html', context)

@login_required
def discussionDelete(request,slug):
    disc=Discussion.objects.get(slug=slug)
    disc.delete()
    posts = Discussion.objects.all()
            #print(posts)
    return redirect('forum')

