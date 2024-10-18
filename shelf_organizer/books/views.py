import re
from django.shortcuts import render
from .models import Book
from .forms import BarcodeScanForm


def call_number_key(call_number):
    """
    Generate a key for sorting call numbers.
    """

    def alphanumeric_sort(text):
        """Convert numbers to zero-padded strings, keep strings in lowercase."""
        if re.match(r"^\d+$", text):
            return text.zfill(10)  # Pad integers with leading zeros
        elif re.match(r"^\d+\.\d+$", text):
            integer_part, fractional_part = text.split(".", 1)
            return f"{integer_part.zfill(10)}.{fractional_part.ljust(10, '0')}"
        else:
            return text.lower()  # Keep strings as lowercase

    parts = re.split(r"\s+", call_number)
    key = []
    for part in parts:
        chunks = re.split(r"(\d+\.\d+|\d+)", part)
        for chunk in chunks:
            if chunk:
                value = alphanumeric_sort(chunk)
                key.append(value)
    return key


def reorder_books(request):
    if request.method == "POST":
        form = BarcodeScanForm(request.POST)
        if form.is_valid():
            barcodes = form.cleaned_data["barcodes"].split()

            books = Book.objects.filter(barcode__in=barcodes)

            original_books = {book.barcode: book for book in books}

            try:
                # Sorting books by call number
                sorted_books = sorted(
                    books, key=lambda x: call_number_key(x.call_number)
                )
            except TypeError as e:
                # Debugging: print details if an error occurs
                for book in books:
                    key = call_number_key(book.call_number)
                    print(
                        f"Call Number: {book.call_number}, Key: {key}, Types: {[type(k) for k in key]}"
                    )
                raise e

            # Store original books
            original_books = {book.barcode: book for book in books}

            # Calculate position changes and prepare the result
            barcode_to_original_position = {
                barcode: index + 1 for index, barcode in enumerate(barcodes)
            }

            result = []
            for new_position, book in enumerate(sorted_books, start=1):
                barcode = book.barcode
                original_position = barcode_to_original_position.get(barcode, None)

                if book:
                    # Check if both position and call number differ
                    if new_position != original_position:
                        position_change = new_position - original_position
                    else:
                        position_change = (
                            0  # No change if call number and position are the same
                        )

                    result.append(
                        {
                            "new_position": new_position,
                            "ordered_call_number": book.call_number,
                            "ordered_barcode": book.barcode,
                            "original_position": original_position,
                            "original_call_number": original_books[barcode].call_number,
                            "original_barcode": book.barcode,
                            "position_change": position_change,
                            "abs_position_change": abs(position_change),
                        }
                    )
                else:
                    result.append(
                        {
                            "new_position": new_position,
                            "ordered_call_number": "Not in Database",
                            "ordered_barcode": barcode,
                            "original_position": original_position,
                            "original_call_number": "Not in Database",
                            "original_barcode": barcode,
                            "position_change": 0,
                            "abs_position_change": 0,
                        }
                    )

            # Generate minimal moves with Bootstrap styling for position
            current_books = barcodes[:]  # Original order of barcodes
            moves = []
            for i, sorted_book in enumerate(sorted_books):
                if current_books[i] != sorted_book.barcode:
                    correct_position = current_books.index(sorted_book.barcode)
                    if i > 0:
                        previous_book = sorted_books[i - 1]
                        moves.append(
                            f"Move {sorted_book.call_number}"
                            f"({sorted_book.barcode}) "
                            f"from position <span class='text-danger'>{barcode_to_original_position[sorted_book.barcode]}</span> "
                            f"after {previous_book.call_number} "
                            f"({previous_book.barcode})."
                        )
                    else:
                        moves.append(
                            f"Move {sorted_book.call_number}"
                            f"({sorted_book.barcode}) "
                            f"from position {barcode_to_original_position[sorted_book.barcode]} "
                            f"to the front."
                        )
                    # Simulate moving the book in the current_books list
                    current_books.insert(i, current_books.pop(correct_position))

            # Render the results and the minimal moves
            return render(
                request, "books/result.html", {"result": result, "moves": moves}
            )

    else:
        form = BarcodeScanForm()

    return render(request, "books/reorder_books.html", {"form": form})
