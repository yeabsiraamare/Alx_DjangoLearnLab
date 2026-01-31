## Retrieve Book

```python
from bookshelf.models import Book

# Retrieve all books
Book.objects.all()

# Retrieve specific book attributes
book = Book.objects.get(title="1984")
book.title, book.author, book.publication_year