from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..models import Book


@login_required
def books(request):
    return render(request, "books/books.html", {"books": Book.objects.all()})
