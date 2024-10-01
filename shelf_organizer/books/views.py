from django.shortcuts import render
from .models import Book
from .forms import BarcodeScanForm

def reorder_books(request):
    if request.method == 'POST':
        form = BarcodeScanForm(request.POST)
        if form.is_valid():
            barcodes = form.cleaned_data['barcodes'].split()
            books = Book.objects.filter(barcode__in=barcodes)

            # Create original list with position, call number, and barcode
            original_books = [(i + 1, book.call_number, book.barcode) for i, book in enumerate(books)]

            # Sort books by call number
            sorted_books = sorted(books, key=lambda x: x.call_number)

            # Create the result with the position, sorted call number, barcode, original call number, and position change
            result = []
            for i, sorted_book in enumerate(sorted_books):
                for index, original_book in enumerate(books):
                    if original_book.barcode == sorted_book.barcode:
                        original_position = index + 1
                        new_position = i + 1
                        position_change = new_position - original_position
                        result.append((
                            new_position,  # New position
                            sorted_book.call_number,  # Ordered call number
                            sorted_book.barcode,  # Ordered barcode
                            original_books[index][1],  # Original call number
                            original_books[index][2],  # Original barcode
                            position_change,  # Position change
                            abs(position_change)  # Absolute value of position change
                        ))

            return render(request, 'books/result.html', {'result': result})
    else:
        form = BarcodeScanForm()

    return render(request, 'books/reorder_books.html', {'form': form})
