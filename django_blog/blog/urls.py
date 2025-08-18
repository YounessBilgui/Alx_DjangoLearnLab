from django.urls import path
from .views import PostListView, PostDetailView, add_comment

app_name = 'blog'

urlpatterns = [
    path('', PostListView.as_view(), name='post-list'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:pk>/comments/new/', add_comment, name='add-comment'),
]
