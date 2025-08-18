from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .models import Post, Comment
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class PostListView(ListView):
	model = Post
	template_name = 'blog/post_list.html'
	context_object_name = 'posts'


class PostDetailView(DetailView):
	model = Post
	template_name = 'blog/post_detail.html'
	context_object_name = 'post'


@login_required
def add_comment(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == 'POST':
		content = request.POST.get('content')
		if content:
			Comment.objects.create(post=post, author=request.user, content=content)
		return redirect(f'/posts/{post.id}/')
	return redirect(f'/posts/{post.id}/')

# Create your views here.
