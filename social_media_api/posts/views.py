from rest_framework import viewsets, permissions, filters, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer

class IsAuthorOrReadOnly(permissions.BasePermission):
	def has_object_permission(self, request, view, obj):
		if request.method in permissions.SAFE_METHODS:
			return True
		return getattr(obj, 'author_id', None) == request.user.id

class PostViewSet(viewsets.ModelViewSet):
	queryset = Post.objects.all().select_related('author').prefetch_related('comments__author')
	serializer_class = PostSerializer
	permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]
	filter_backends = [filters.SearchFilter]
	search_fields = ['title', 'content']

	def perform_create(self, serializer):
		serializer.save(author=self.request.user)

class CommentViewSet(viewsets.ModelViewSet):
	queryset = Comment.objects.all().select_related('author', 'post')
	serializer_class = CommentSerializer
	permission_classes = [permissions.IsAuthenticated, IsAuthorOrReadOnly]

	def perform_create(self, serializer):
		serializer.save(author=self.request.user)

	def get_queryset(self):
		queryset = super().get_queryset()
		post_id = self.request.query_params.get('post')
		if post_id:
			queryset = queryset.filter(post_id=post_id)
		return queryset

class FeedView(generics.ListAPIView):
	serializer_class = PostSerializer
	permission_classes = [permissions.IsAuthenticated]
	filter_backends = [filters.SearchFilter]
	search_fields = ['title', 'content']

	def get_queryset(self):
		user = self.request.user
		followed_ids = user.following.values_list('id', flat=True)
		return Post.objects.filter(author_id__in=followed_ids).select_related('author').prefetch_related('comments__author')
