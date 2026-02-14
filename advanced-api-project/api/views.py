from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer


"""
BookListView:
    - Handles GET requests to list all books.
    - Uses ListAPIView for read-only listing.
    - Public access allowed.
"""
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


"""
BookDetailView:
    - Handles GET requests for a single book by ID.
    - Uses RetrieveAPIView for read-only detail view.
    - Public access allowed.
"""
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.AllowAny]


"""
BookCreateView:
    - Handles POST requests to create a new book.
    - Restricted to authenticated users.
    - Custom behavior added using perform_create().
"""
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        """
        Custom creation logic:
        - You can attach the user who created the book
        - You can log creation events
        - You can modify data before saving
        """
        serializer.save()  # Save normally for now


"""
BookUpdateView:
    - Handles PUT/PATCH requests to update an existing book.
    - Restricted to authenticated users.
    - Custom behavior added using perform_update().
"""
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_update(self, serializer):
        """
        Custom update logic:
        - You can enforce additional validation
        - You can track who updated the book
        - You can modify fields before saving
        """
        serializer.save()  # Save normally for now


"""
BookDeleteView:
    - Handles DELETE requests to remove a book.
    - Restricted to authenticated users.
"""
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticated]
