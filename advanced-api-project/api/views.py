from rest_framework import generics, permissions, filters
from django_filters import rest_framework as django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Book
from .serializers import BookSerializer

# BookListView: Retrieve all books (read-only for unauthenticated users)
class BookListView(generics.ListAPIView):
	"""
	API endpoint to list all books.
	Accessible to all users (read-only).
	"""
	queryset = Book.objects.all()
	serializer_class = BookSerializer
	permission_classes = [permissions.AllowAny]
	# Enable filtering, searching, and ordering
	filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
	# Filtering by title, author (id), and publication_year
	filterset_fields = ['title', 'author', 'publication_year']
	# Searching by title and author's name (traverse relationship)
	search_fields = ['title', 'author__name']
	# Ordering by title and publication_year
	ordering_fields = ['title', 'publication_year']
	ordering = ['title']  # Default ordering
	"""
	Filtering: /api/books/?title=BookTitle&author=1&publication_year=2020
	Searching: /api/books/?search=SomeText
	Ordering:  /api/books/?ordering=title or /api/books/?ordering=-publication_year
	"""

# BookDetailView: Retrieve a single book by ID (read-only for unauthenticated users)
class BookDetailView(generics.RetrieveAPIView):
	"""
	API endpoint to retrieve a single book by its ID.
	Accessible to all users (read-only).
	"""
	queryset = Book.objects.all()
	serializer_class = BookSerializer
	permission_classes = [permissions.AllowAny]

# BookCreateView: Create a new book (authenticated users only)
class BookCreateView(generics.CreateAPIView):
	"""
	API endpoint to create a new book.
	Only authenticated users can create books.
	Custom validation is handled by BookSerializer.
	"""
	queryset = Book.objects.all()
	serializer_class = BookSerializer
	permission_classes = [permissions.IsAuthenticated]

# BookUpdateView: Update an existing book (authenticated users only)
class BookUpdateView(generics.UpdateAPIView):
	"""
	API endpoint to update an existing book.
	Only authenticated users can update books.
	Custom validation is handled by BookSerializer.
	"""
	queryset = Book.objects.all()
	serializer_class = BookSerializer
	permission_classes = [permissions.IsAuthenticated]

# BookDeleteView: Delete a book (authenticated users only)
class BookDeleteView(generics.DestroyAPIView):
	"""
	API endpoint to delete a book.
	Only authenticated users can delete books.
	"""
	queryset = Book.objects.all()
	serializer_class = BookSerializer
	permission_classes = [permissions.IsAuthenticated]

	# BookBulkUpdateView: Custom endpoint for bulk update
	class BookBulkUpdateView(APIView):
		"""
		API endpoint to bulk update books.
		Only authenticated users can access.
		"""
		permission_classes = [IsAuthenticated]

		def put(self, request):
			updates = request.data.get('updates', [])
			updated_books = []
			for update in updates:
				try:
					book = Book.objects.get(pk=update['id'])
					serializer = BookSerializer(book, data=update, partial=True)
					if serializer.is_valid():
						serializer.save()
						updated_books.append(serializer.data)
				except Book.DoesNotExist:
					continue
			return Response({'updated': updated_books}, status=status.HTTP_200_OK)

	# BookBulkDeleteView: Custom endpoint for bulk delete
	class BookBulkDeleteView(APIView):
		"""
		API endpoint to bulk delete books.
		Only authenticated users can access.
		"""
		permission_classes = [IsAuthenticated]

		def delete(self, request):
			ids = request.data.get('ids', [])
			deleted = []
			for book_id in ids:
				try:
					book = Book.objects.get(pk=book_id)
					book.delete()
					deleted.append(book_id)
				except Book.DoesNotExist:
					continue
			return Response({'deleted': deleted}, status=status.HTTP_200_OK)
