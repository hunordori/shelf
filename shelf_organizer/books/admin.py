from django.contrib import admin
from books.models import Book
from django.contrib.admin import ModelAdmin


@admin.register(Book)
class BookAdmin(ModelAdmin):
    model = Book
    list_display = ("title", "barcode", "call_number")
    ordering = ("title",)
    search_fields = ("title", "barcode", "call_number")
