from rest_framework import generics, permissions
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
