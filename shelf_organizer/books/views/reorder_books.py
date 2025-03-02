import re
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from ..models import Book
from ..forms import BarcodeScanForm

def call_number_key(call_number):
    """
    Generate a key for sorting Library of Congress (LC) call numbers.
    - First section (letters) is sorted alphabetically.
    - Second section (numbers) is treated as a decimal.
    - Third section (Cutter numbers) is stripped of dots and split piece-by-piece.
    - Remaining sections are sorted numerically/alphabetically.
    """

    def alphanumeric_sort(text):
        """Process numbers and Cutter numbers correctly."""

        # Handle section numbers with decimals (25.3 → 25.3)
        if re.match(r"^\d+\.\d+$", text):
            return float(text)

        # Handle whole numbers (98 → 98)
        elif re.match(r"^\d+$", text):
            return int(text)

        # Handle Cutter numbers (e.g., C598, C8, B3912, B392)
        elif re.match(r"^[A-Za-z]+\d+$", text):
            letter_part = "".join(re.findall(r"[A-Za-z]+", text))
            number_part = "".join(re.findall(r"\d+", text))
            return [letter_part.lower()] + list(number_part)  # Split numbers digit-by-digit

        else:
            return text.lower()  # Alphabetical sorting for letters

    # **Step 1**: Split call number into sections
    parts = re.split(r"\s+", call_number)

    key = []
    for i, part in enumerate(parts):
        # **Step 2**: Treat all Cutter numbers (third section) as if they never had a dot
        if i == 2:  # Cutter section
            part = part.replace(".", "")  # Remove dots from Cutter numbers

        # **Step 3**: Split each section into meaningful groups
        chunks = re.split(r"(\d+\.\d+|\d+|[A-Za-z]+\d+)", part)

        for chunk in chunks:
            if chunk:
                value = alphanumeric_sort(chunk)
                if isinstance(value, list):
                    key.extend(value)
                else:
                    key.append(value)

    return key





@login_required
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
