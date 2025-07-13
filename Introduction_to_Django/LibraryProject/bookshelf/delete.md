# Delete Operation

This document demonstrates how to delete a Book instance using Django's ORM.

## Command Used:
```python
from bookshelf.models import Book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
print("Book deleted successfully")

# Verify deletion by checking all books
all_books = Book.objects.all()
print(f"Total books remaining: {all_books.count()}")
```

## Expected Output:
```
(1, {'bookshelf.Book': 1})
Book deleted successfully
Total books remaining: 0
```

The `delete()` method removes the book instance from the database. The method returns a tuple containing the number of objects deleted and a dictionary with the breakdown of deletions by model.
