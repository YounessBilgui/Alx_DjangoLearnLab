from django.urls import path
from django.contrib.auth import views as auth_views
from .views import (
    PostListView,
    PostSearchView,
    TagPostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    add_comment,
    register,
    profile,
    login_view,
    logout_view,
)

app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('search/', PostSearchView.as_view(), name='post-search'),
    path('tags/<slug:slug>/', TagPostListView.as_view(), name='tag-posts'),
    path('posts/new/', PostCreateView.as_view(), name='post-create'),
    path('posts/<int:pk>/edit/', PostUpdateView.as_view(), name='post-edit'),
    path('posts/<int:pk>/delete/', PostDeleteView.as_view(), name='post-delete'),
    path('posts/<int:pk>/comments/new/', add_comment, name='add-comment'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile, name='profile'),
]
