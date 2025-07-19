
# Sample queries for Django model relationships
from relationship_app.models import Author, Book, Library, Librarian

# Query all books by a specific author
def books_by_author(author_name):
    author = Author.objects.get(name=author_name)
    return Book.objects.filter(author=author)

# List all books in a library
def books_in_library(library_name):
    library = Library.objects.get(name=library_name)
    return library.books.all()

# Retrieve the librarian for a library
def librarian_for_library(library_name):
    library = Library.objects.get(name=library_name)
    return Librarian.objects.get(library=library)

# Example usage (replace with actual names in your DB)
if __name__ == "__main__":
    print("Books by Author:", list(books_by_author("Author Name")))
    print("Books in Library:", list(books_in_library("Library Name")))
    print("Librarian for Library:", librarian_for_library("Library Name"))
