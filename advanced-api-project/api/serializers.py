from rest_framework import serializers
from .models import Author, Book
from datetime import datetime


# BookSerializer is responsible for converting Book model instances
# to and from primitive data types (e.g., JSON).
# It includes all fields of the Book model.
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

    # Custom validation ensures that publication_year is not in the future.
    def validate_publication_year(self, value):
        current_year = datetime.now().year
        if value > current_year:
            # Raise a validation error if the year is greater than the current year.
            raise serializers.ValidationError(
                "Publication year cannot be in the future."
            )
        return value


# AuthorSerializer represents an Author along with their related books.
# It uses a nested BookSerializer to serialize the one-to-many relationship.
class AuthorSerializer(serializers.ModelSerializer):
    # The 'books' field uses the related_name defined in the Book model.
    # many=True indicates that an author can have multiple books.
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
        # This shows how the relationship is handled:
        # 'books' is a nested representation of all Book instances
        # linked to this Author via the foreign key.
