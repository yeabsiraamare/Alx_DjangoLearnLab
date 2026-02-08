from django.db import models

class Author(models.Model):
    """
    Author model represents a book author.
    One author can have many books.
    """
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Book(models.Model):
    """
    Book model represents a single book.
    Each book is linked to one Author via a ForeignKey.
    """
    title = models.CharField(max_length=255)
    publication_year = models.IntegerField()
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books'  # used for nested serialization
    )

    def __str__(self):
        return f"{self.title} ({self.publication_year})"
