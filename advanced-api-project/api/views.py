from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Author, Book


class BookAPITests(APITestCase):
    """
    Test suite for Book API endpoints:
    - CRUD operations
    - Filtering, searching, ordering
    - Permissions and authentication
    """

    def setUp(self):
        # Create a user for authenticated requests
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword123"
        )

        # Create authors
        self.author1 = Author.objects.create(name="Chinua Achebe")
        self.author2 = Author.objects.create(name="George Orwell")

        # Create books
        self.book1 = Book.objects.create(
            title="Things Fall Apart",
            publication_year=1958,
            author=self.author1
        )
        self.book2 = Book.objects.create(
            title="No Longer at Ease",
            publication_year=1960,
            author=self.author1
        )
        self.book3 = Book.objects.create(
            title="1984",
            publication_year=1949,
            author=self.author2
        )

        # Common URLs
        self.list_url = reverse('book-list')
        self.create_url = reverse('book-create')
        self.detail_url = reverse('book-detail', args=[self.book1.id])
        self.update_url = reverse('book-update', args=[self.book1.id])
        self.delete_url = reverse('book-delete', args=[self.book1.id])

    # ---------- READ (List & Detail) ----------

    def test_list_books_is_public(self):
        """
        Anyone should be able to list books (read-only access).
        """
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)

    def test_retrieve_single_book_is_public(self):
        """
        Anyone should be able to retrieve a single book.
        """
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)

    # ---------- CREATE ----------

    def test_create_book_requires_authentication(self):
        """
        Unauthenticated users should NOT be able to create a book.
        """
        data = {
            "title": "New Book",
            "publication_year": 2020,
            "author": self.author1.id,
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_book_authenticated(self):
        """
        Authenticated users should be able to create a book.
        """
        self.client.login(username="testuser", password="testpassword123")
        data = {
            "title": "New Auth Book",
            "publication_year": 2020,
            "author": self.author1.id,
        }
        response = self.client.post(self.create_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4)
        self.assertEqual(Book.objects.last().title, "New Auth Book")

    # ---------- UPDATE ----------

    def test_update_book_requires_authentication(self):
        """
        Unauthenticated users should NOT be able to update a book.
        """
        data = {
            "title": "Updated Title",
            "publication_year": self.book1.publication_year,
            "author": self.book1.author.id,
        }
        response = self.client.put(self.update_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_book_authenticated(self):
        """
        Authenticated users should be able to update a book.
        """
        self.client.login(username="testuser", password="testpassword123")
        data = {
            "title": "Updated Title",
            "publication_year": self.book1.publication_year,
            "author": self.book1.author.id,
        }
        response = self.client.put(self.update_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Title")

    # ---------- DELETE ----------

    def test_delete_book_requires_authentication(self):
        """
        Unauthenticated users should NOT be able to delete a book.
        """
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(Book.objects.filter(id=self.book1.id).exists())

    def test_delete_book_authenticated(self):
        """
        Authenticated users should be able to delete a book.
        """
        self.client.login(username="testuser", password="testpassword123")
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book1.id).exists())

    # ---------- FILTERING ----------

    def test_filter_books_by_title(self):
        """
        Filter books by exact title using query params.
        """
        response = self.client.get(self.list_url, {'title': '1984'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], '1984')

    def test_filter_books_by_author(self):
        """
        Filter books by author ID.
        """
        response = self.client.get(self.list_url, {'author': self.author1.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_filter_books_by_publication_year(self):
        """
        Filter books by publication_year.
        """
        response = self.client.get(self.list_url, {'publication_year': 1958})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['title'], 'Things Fall Apart')

    # ---------- SEARCH ----------

    def test_search_books_by_title(self):
        """
        Search books by partial title.
        """
        response = self.client.get(self.list_url, {'search': 'Fall'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)
        titles = [book['title'] for book in response.data]
        self.assertIn('Things Fall Apart', titles)

    def test_search_books_by_author_name(self):
        """
        Search books by author name.
        """
        response = self.client.get(self.list_url, {'search': 'Achebe'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    # ---------- ORDERING ----------

    def test_order_books_by_title(self):
        """
        Order books by title ascending.
        """
        response = self.client.get(self.list_url, {'ordering': 'title'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book['title'] for book in response.data]
        self.assertEqual(titles, sorted(titles))

    def test_order_books_by_publication_year_desc(self):
        """
        Order books by publication_year descending.
        """
        response = self.client.get(self.list_url, {'ordering': '-publication_year'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book['publication_year'] for book in response.data]
        self.assertEqual(years, sorted(years, reverse=True))
