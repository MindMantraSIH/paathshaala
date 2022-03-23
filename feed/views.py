from django.shortcuts import render
from .models import Post
from profiles.models import School,User
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required()
def school_feed(request, slug):
    context = {}
    user = request.user
    if user.is_student:
        context['student'] = user
    school = School.objects.filter(user__slug = slug)[0]
    posts = Post.objects.filter(school = school)
    context['posts'] = posts
    context['school'] = school
    if request.method == 'POST':
        print('HELLLO')
        title = request.POST.get('title')
        content = request.POST.get('content')
        im = request.POST.get('image')
        post = Post.objects.create(title=title.strip(),content=content.strip(),school=request.user.school,image=im)
        post.save()
        return render(request, 'feed/school_feed.html',context)
    
    
   
    return render(request, 'feed/school_feed.html',context)