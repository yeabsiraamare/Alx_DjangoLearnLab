from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from .models import Book
from django import forms


class SearchForm(forms.Form):
    query = forms.CharField(required=False, max_length=100)


@permission_required('bookshelf.can_view', raise_exception=True)
def book_list(request):
    form = SearchForm(request.GET or None)
    books = Book.objects.all()

    if form.is_valid():
        query = form.cleaned_data['query']
        if query:
            # SAFE ORM query (prevents SQL injection)
            books = books.filter(title__icontains=query)

    return render(request, 'bookshelf/book_list.html', {
        'books': books,
        'form': form
    })


@permission_required('bookshelf.can_create', raise_exception=True)
def create_book(request):
    return render(request, 'bookshelf/create_book.html')


@permission_required('bookshelf.can_edit', raise_exception=True)
def edit_book(request):
    return render(request, 'bookshelf/edit_book.html')


@permission_required('bookshelf.can_delete', raise_exception=True)
def delete_book(request):
    return render(request, 'bookshelf/delete_book.html')
