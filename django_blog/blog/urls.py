from django.urls import path
from django.contrib.auth import views as auth_views
from .views import PostListView, PostDetailView, add_comment, register, profile, login_view, logout_view

app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:pk>/comments/new/', add_comment, name='add-comment'),
    path('register/', register, name='register'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile, name='profile'),
]
