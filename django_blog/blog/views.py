from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView
from .models import Post, Comment
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import RegistrationForm, ProfileForm
from django.contrib.auth import get_user_model

User = get_user_model()


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

def register(request):
	if request.method == 'POST':
		form = RegistrationForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, 'Registration successful.')
			return redirect('blog:post-list')
	else:
		form = RegistrationForm()
	return render(request, 'registration/register.html', {'form': form})


@login_required
def profile(request):
	user = request.user
	if request.method == 'POST':
		p_form = ProfileForm(request.POST, instance=user.profile)
		if p_form.is_valid():
			p_form.save()
			messages.success(request, 'Profile updated.')
			return redirect('blog:profile')
	else:
		p_form = ProfileForm(instance=user.profile)
	return render(request, 'registration/profile.html', {'p_form': p_form})


def login_view(request):
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		user = authenticate(request, username=username, password=password)
		if user is not None:
			login(request, user)
			return redirect('blog:post-list')
		messages.error(request, 'Invalid credentials.')
	return render(request, 'registration/login.html', {})


def logout_view(request):
	if request.method in ['GET', 'POST']:
		logout(request)
		return redirect('blog:post-list')
	return redirect('blog:post-list')

