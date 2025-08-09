from django.urls import path
from .views import (
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    BookDeleteView,
    BookBulkUpdateView,
    BookBulkDeleteView,
)

urlpatterns = [
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('books/create/', BookCreateView.as_view(), name='book-create'),
    path('books/<int:pk>/update/', BookUpdateView.as_view(), name='book-update'),
    path('books/<int:pk>/delete/', BookDeleteView.as_view(), name='book-delete'),
    path('books/update/', BookBulkUpdateView.as_view(), name='books-update'),
    path('books/delete/', BookBulkDeleteView.as_view(), name='books-delete'),
]

"""
API Endpoints:
- GET    /books/                : List all books (any user)
- GET    /books/<pk>/           : Retrieve a book by ID (any user)
- POST   /books/create/         : Create a new book (authenticated only)
- PUT    /books/<pk>/update/    : Update a book (authenticated only)
- DELETE /books/<pk>/delete/    : Delete a book (authenticated only)
"""
