# Create Operation

This document demonstrates how to create a Book instance using Django's ORM.

## Command Used:
```python
from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
print(f"Book created: {book}")
```

## Expected Output:
```
Book created: 1984
```

The `create()` method creates a new Book instance and saves it to the database in one operation. The book object is returned and can be used immediately.
