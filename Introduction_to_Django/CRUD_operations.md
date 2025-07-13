# CRUD Operations Documentation

This document provides a comprehensive overview of Create, Read, Update, and Delete operations performed on the Book model using Django's ORM through the Django shell.

## Setup
All operations were performed in the Django shell, accessed via:
```bash
python manage.py shell
```

## 1. Create Operation

### Command:
```python
from bookshelf.models import Book
book = Book.objects.create(title="1984", author="George Orwell", publication_year=1949)
print(f"Book created: {book}")
```

### Output:
```
Book created: 1984
```

### Description:
Creates a new Book instance with the specified title, author, and publication year. The `create()` method both instantiates and saves the object to the database.

## 2. Retrieve Operation

### Command:
```python
from bookshelf.models import Book
book = Book.objects.get(title="1984")
print(f"Title: {book.title}")
print(f"Author: {book.author}")
print(f"Publication Year: {book.publication_year}")
```

### Output:
```
Title: 1984
Author: George Orwell
Publication Year: 1949
```

### Description:
Retrieves the book with the title "1984" and displays all its attributes. The `get()` method returns a single instance that matches the query.

## 3. Update Operation

### Command:
```python
from bookshelf.models import Book
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
print(f"Updated book title: {book.title}")
```

### Output:
```
Updated book title: Nineteen Eighty-Four
```

### Description:
Updates the title of the existing book from "1984" to "Nineteen Eighty-Four". The changes are persisted to the database using the `save()` method.

## 4. Delete Operation

### Command:
```python
from bookshelf.models import Book
book = Book.objects.get(title="Nineteen Eighty-Four")
book.delete()
print("Book deleted successfully")

# Verify deletion
all_books = Book.objects.all()
print(f"Total books remaining: {all_books.count()}")
```

### Output:
```
(1, {'bookshelf.Book': 1})
Book deleted successfully
Total books remaining: 0
```

### Description:
Deletes the book from the database. The `delete()` method returns a tuple showing the number of objects deleted. The verification confirms that no books remain in the database.

## Summary
All CRUD operations were successfully performed on the Book model:
- **Create**: Added a new book "1984" by George Orwell
- **Read**: Retrieved and displayed book details
- **Update**: Changed the title to "Nineteen Eighty-Four"
- **Delete**: Removed the book from the database

These operations demonstrate the basic functionality of Django's ORM for database interactions.
