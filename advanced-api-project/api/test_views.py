from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Author, Book
from django.contrib.auth import get_user_model

class BookAPITestCase(APITestCase):
    """
    Unit tests for Book API endpoints, including CRUD, filtering, searching, ordering, and permissions.
    Run with: python manage.py test api
    """
    def setUp(self):
        self.user = get_user_model().objects.create_user(username='testuser', password='testpass')
        self.author = Author.objects.create(name='Author One')
        self.book1 = Book.objects.create(title='Book One', publication_year=2020, author=self.author)
        self.book2 = Book.objects.create(title='Book Two', publication_year=2021, author=self.author)
        self.client = APIClient()

    def test_list_books(self):
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_book_authenticated(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('book-create')
        data = {'title': 'Book Three', 'publication_year': 2022, 'author': self.author.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 3)

    def test_create_book_unauthenticated(self):
        url = reverse('book-create')
        data = {'title': 'Book Four', 'publication_year': 2022, 'author': self.author.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_book_authenticated(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('book-update', args=[self.book1.id])
        data = {'title': 'Book One Updated', 'publication_year': 2020, 'author': self.author.id}
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Book One Updated')

    def test_delete_book_authenticated(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('book-delete', args=[self.book2.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 1)

    def test_filter_books_by_title(self):
        url = reverse('book-list') + '?title=Book One'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Book One')

    def test_search_books_by_title(self):
        url = reverse('book-list') + '?search=Book Two'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Book Two')

    def test_order_books_by_publication_year(self):
        url = reverse('book-list') + '?ordering=-publication_year'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['publication_year'], 2021)

    def test_permissions(self):
        # Unauthenticated user cannot create, update, or delete
        create_url = reverse('book-create')
        update_url = reverse('book-update', args=[self.book1.id])
        delete_url = reverse('book-delete', args=[self.book1.id])
        data = {'title': 'Should Fail', 'publication_year': 2020, 'author': self.author.id}
        self.assertEqual(self.client.post(create_url, data).status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.client.put(update_url, data).status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.client.delete(delete_url).status_code, status.HTTP_403_FORBIDDEN)

"""
Testing strategy:
- Each test simulates API requests and checks status codes and response data.
- CRUD, filtering, searching, ordering, and permissions are covered.
- Run tests with: python manage.py test api
"""
