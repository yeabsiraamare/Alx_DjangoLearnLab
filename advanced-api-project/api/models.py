from django.db import models

# Author model represents a writer who can have multiple books.
# This is the "one" side of a one-to-many relationship with Book.
class Author(models.Model):
    # Stores the full name of the author.
    name = models.CharField(max_length=255)

    def __str__(self):
        # Helpful string representation for admin and shell.
        return self.name


# Book model represents a single book written by an Author.
# Each book is linked to exactly one Author via a foreign key.
class Book(models.Model):
    # Title of the book.
    title = models.CharField(max_length=255)

    # Year the book was published.
    publication_year = models.IntegerField()

    # Foreign key to Author creates a one-to-many relationship:
    # one Author can have many Books.
    author = models.ForeignKey(
        Author,
        related_name='books',  # used for reverse lookup in serializers
        on_delete=models.CASCADE
    )

    def __str__(self):
        # Helpful string representation for admin and shell.
        return f"{self.title} ({self.publication_year})"
