from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from books.models import Book


def welcome(request):
    if request.user.is_authenticated:
        context = {"Books": Book.objects.all()}
    else:
        context = {}
    return render(request, "welcome.html", context)
