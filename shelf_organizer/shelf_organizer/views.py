from django.shortcuts import render

from books.models import Book


def welcome(request):
    if request.user.is_authenticated:
        context = {"Books": Book.objects.all()}
    else:
        context = {}
    return render(request, "welcome.html", context)

def help(request):
    return render(request, "help.html")
