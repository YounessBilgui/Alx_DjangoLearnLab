# Update Operation

This document demonstrates how to update a Book instance using Django's ORM.

## Command Used:
```python
from bookshelf.models import Book
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
print(f"Updated book title: {book.title}")
```

## Expected Output:
```
Updated book title: Nineteen Eighty-Four
```

The update operation involves retrieving the book object, modifying its attributes, and calling the `save()` method to persist the changes to the database.
