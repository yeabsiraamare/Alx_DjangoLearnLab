# Advanced API Project — Task 2

This section implements CRUD operations for the Book model using Django REST Framework generic views.

## Views Implemented

### BookListView
- Lists all books
- Public access

### BookDetailView
- Retrieves a single book by ID
- Public access

### BookCreateView
- Creates a new book
- Requires authentication

### BookUpdateView
- Updates an existing book
- Requires authentication

### BookDeleteView
- Deletes a book
- Requires authentication

## URL Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /api/books/ | List all books |
| GET | /api/books/<pk>/ | Retrieve one book |
| POST | /api/books/create/ | Create a book |
| PUT/PATCH | /api/books/<pk>/update/ | Update a book |
| DELETE | /api/books/<pk>/delete/ | Delete a book |

## Permissions
- Read-only endpoints are public.
- Create, Update, Delete require authentication.

## Custom Behavior
- Validation handled in serializers.
- `perform_create` and `perform_update` allow further customization.


## Filtering, Searching, and Ordering

### Filtering
You can filter books by:
- title
- author (ID)
- publication_year

Example:
GET /api/books/?title=Things Fall Apart

### Searching
Search across title and author name:
GET /api/books/?search=achebe

### Ordering
Order results by title or publication_year:
GET /api/books/?ordering=title
GET /api/books/?ordering=-publication_year

