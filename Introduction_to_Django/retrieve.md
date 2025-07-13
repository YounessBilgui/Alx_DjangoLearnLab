# Retrieve Operation

This document demonstrates how to retrieve a Book instance using Django's ORM.

## Command Used:
```python
from bookshelf.models import Book
book = Book.objects.get(title="1984")
print(f"Title: {book.title}")
print(f"Author: {book.author}")
print(f"Publication Year: {book.publication_year}")
```

## Expected Output:
```
Title: 1984
Author: George Orwell
Publication Year: 1949
```

The `get()` method retrieves a single Book instance that matches the given criteria. If no book is found or multiple books match, it will raise an exception.
