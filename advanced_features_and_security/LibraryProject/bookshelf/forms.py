from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'publication_year']
        # All fields are validated and sanitized by Django forms

class ExampleForm(forms.Form):
    example_field = forms.CharField(max_length=100)
    # This form demonstrates secure input handling and validation
