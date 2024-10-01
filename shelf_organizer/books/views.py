from django.shortcuts import render
from .models import Book
from .forms import BarcodeScanForm

def reorder_books(request):
    if request.method == 'POST':
        form = BarcodeScanForm(request.POST)
        if form.is_valid():
            barcodes = form.cleaned_data['barcodes'].split()
            books = Book.objects.filter(barcode__in=barcodes)

            # Normalize call numbers and sort books
            sorted_books = sorted(books, key=lambda x: x.call_number)

            # Create the result to display
            result = [(book.call_number, book.barcode) for book in sorted_books]

            return render(request, 'books/result.html', {'result': result})
    else:
        form = BarcodeScanForm()

    return render(request, 'books/reorder_books.html', {'form': form})
