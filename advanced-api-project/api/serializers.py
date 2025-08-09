from rest_framework import serializers
from .models import Author, Book
from datetime import date


class BookSerializer(serializers.ModelSerializer):
    """
    Serializer for the Book model.
    Serializes all fields and validates that publication_year is not in the future.
    """
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

    def validate_publication_year(self, value):
        """
        Ensure publication_year is not in the future.
        """
        current_year = date.today().year
        if value > current_year:
            raise serializers.ValidationError(f"Publication year cannot be in the future (>{current_year}).")
        return value


class AuthorSerializer(serializers.ModelSerializer):
    """
    Serializer for the Author model.
    Includes the author's name and a nested list of their books using BookSerializer.
    Demonstrates handling of nested relationships in DRF.
    """
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']

    # The 'books' field uses the related_name from the Book model's ForeignKey to Author.
    # This allows us to serialize all books for a given author in a nested structure.
