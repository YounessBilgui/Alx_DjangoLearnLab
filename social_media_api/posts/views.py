from rest_framework import viewsets, permissions, filters
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
