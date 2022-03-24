from django.shortcuts import redirect, render, get_object_or_404
from .models import Post
from profiles.models import School,User
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
import json
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
	context['user'] = user
	if request.method == 'POST':
		if 'image' in request.FILES:
			im = request.FILES['image']
		else:
			im = None
		title = request.POST.get('title')
		content = request.POST.get('content')
		post = Post.objects.create(title=title.strip(),content=content.strip(),school=request.user.school,image=im)
		post.save()
		return render(request, 'feed/school_feed.html',context)
	
	
   
	return render(request, 'feed/school_feed.html',context)


def delete_feed_post(request, school, slug):
	post = Post.objects.filter(slug = slug)[0]
	print(post)
	if post.school == request.user.school:
		print('ayy')
		post.delete()
	return redirect('school-feed', school)


def upvote_ajax(request):
	post = get_object_or_404(Post, slug=request.POST.get('post_slug'))
	print(post)
	up_status = ''
	if post.upvote.filter(id=request.user.id).exists():
		post.upvote.remove(request.user)
		up_status = 'disliked'
	else:
		post.upvote.add(request.user)
		up_status = 'liked'
	up_count = post.number_of_upvotes()
	print(up_count)
	ctx = {'up_status':up_status,'up_count':up_count,'post_slug':post.slug}
	return HttpResponse(json.dumps(ctx), content_type='application/json')