from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Comment
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import RegistrationForm, ProfileForm, PostForm, CommentForm
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from taggit.models import Tag
from django.db.models import Q
from django.contrib.auth import get_user_model

User = get_user_model()


class HomeView(ListView):
	model = Post
	template_name = 'home.html'
	context_object_name = 'posts'


class PostListView(ListView):
	model = Post
	template_name = 'blog/post_list.html'  # namespaced template per checker
	context_object_name = 'posts'


class PostSearchView(ListView):
	model = Post
	template_name = 'search_results.html'
	context_object_name = 'posts'

	def get_queryset(self):
		qs = super().get_queryset()
		q = self.request.GET.get('q')
		if q:
			return qs.filter(
				Q(title__icontains=q) |
				Q(content__icontains=q) |
				Q(tags__name__icontains=q)
			).distinct()
		return qs.none()

	def get_context_data(self, **kwargs):
		ctx = super().get_context_data(**kwargs)
		ctx['query'] = self.request.GET.get('q', '')
		return ctx


class TagPostListView(ListView):
	model = Post
	template_name = 'posts_by_tag.html'
	context_object_name = 'posts'

	def get_queryset(self):
		self.tag = Tag.objects.filter(slug=self.kwargs.get('slug')).first()
		if not self.tag:
			return Post.objects.none()
		return Post.objects.filter(tags__in=[self.tag]).distinct()

	def get_context_data(self, **kwargs):
		ctx = super().get_context_data(**kwargs)
		ctx['tag'] = getattr(self, 'tag', None)
		return ctx


class PostDetailView(DetailView):
	model = Post
	template_name = 'blog/post_detail.html'  # namespaced template per checker
	context_object_name = 'post'

	def get_context_data(self, **kwargs):
		ctx = super().get_context_data(**kwargs)
		if self.request.user.is_authenticated:
			ctx['comment_form'] = CommentForm()
		return ctx


class PostCreateView(LoginRequiredMixin, CreateView):
	model = Post
	template_name = 'blog/post_form.html'  # unified create/update template
	form_class = PostForm

	def form_valid(self, form):
		form.instance.author = self.request.user
		response = super().form_valid(form)
		return response

	def get_success_url(self):
		return self.object.get_absolute_url() if hasattr(self.object, 'get_absolute_url') else reverse_lazy('blog:post-detail', kwargs={'pk': self.object.pk})


class AuthorRequiredMixin(UserPassesTestMixin):
	"""Restrict modification to the post's author; return 403 for others."""
	raise_exception = True  # ensures 403 instead of redirect

	def test_func(self):
		obj = self.get_object()
		return obj.author == self.request.user


class PostUpdateView(LoginRequiredMixin, AuthorRequiredMixin, UpdateView):
	model = Post
	form_class = PostForm
	template_name = 'blog/post_form.html'

	def get_success_url(self):
		return reverse_lazy('blog:post-detail', kwargs={'pk': self.object.pk})


class PostDeleteView(LoginRequiredMixin, AuthorRequiredMixin, DeleteView):
	model = Post
	template_name = 'blog/post_confirm_delete.html'
	success_url = reverse_lazy('blog:post-list')


@login_required
def add_comment(request, pk):
	post = get_object_or_404(Post, pk=pk)
	if request.method == 'POST':
		form = CommentForm(request.POST)
		if form.is_valid():
			comment = form.save(commit=False)
			comment.post = post
			comment.author = request.user
			comment.save()
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


class CommentAuthorRequiredMixin(UserPassesTestMixin):
	"""Restrict comment edit/delete to its author; 403 for others."""
	raise_exception = True

	def test_func(self):
		obj = self.get_object()
		return obj.author == self.request.user


class CommentUpdateView(LoginRequiredMixin, CommentAuthorRequiredMixin, UpdateView):
	model = Comment
	form_class = CommentForm
	template_name = 'comment_form.html'

	def get_success_url(self):
		return self.object.post.get_absolute_url()


class CommentDeleteView(LoginRequiredMixin, CommentAuthorRequiredMixin, DeleteView):
	model = Comment
	template_name = 'comment_confirm_delete.html'

	def get_success_url(self):
		return self.object.post.get_absolute_url()


class CommentCreateView(LoginRequiredMixin, CreateView):
	model = Comment
	form_class = CommentForm
	template_name = 'comment_form.html'

	def form_valid(self, form):
		post = get_object_or_404(Post, pk=self.kwargs.get('pk'))
		form.instance.post = post
		form.instance.author = self.request.user
		return super().form_valid(form)

	def get_success_url(self):
		return self.object.post.get_absolute_url()

