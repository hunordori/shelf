import csv
from django.shortcuts import render, redirect
from django.contrib import messages
from ..models import Book


def import_books(request):
    if request.method == "POST" and "import_file" in request.FILES:
        file = request.FILES["import_file"]

        if not file.name.endswith(".csv"):
            messages.error(request, "Please upload a CSV file.")
            return redirect("import_books")

        try:
            reader = csv.DictReader(file.read().decode("utf-8").splitlines())

            # Debugging: print CSV headers
            print(
                "CSV Headers:", reader.fieldnames
            )  # Check what headers are actually read

            # Acceptable column names
            field_mapping = {
                "title": ["title"],
                "barcode": ["barcode"],
                "call_number": ["call_number", "call number"],
            }

            # Check if all required columns are present
            actual_fields = set(reader.fieldnames)
            for key, alternatives in field_mapping.items():
                if not any(field in actual_fields for field in alternatives):
                    messages.error(
                        request,
                        "CSV file must contain title, barcode, and call_number columns.",
                    )
                    return redirect("import_books")

            # Rename fields to standard names
            renamed_rows = []
            for row in reader:
                renamed_row = {
                    "title": row.get("title"),
                    "barcode": row.get("barcode"),
                    "call_number": row.get("call_number") or row.get("call number"),
                }
                renamed_rows.append(renamed_row)

            # Import data
            for row in renamed_rows:
                Book.objects.update_or_create(
                    barcode=row["barcode"],
                    defaults={"title": row["title"], "call_number": row["call_number"]},
                )
            messages.success(request, "Books imported successfully.")

        except Exception as e:
            messages.error(request, f"Error during import: {str(e)}")

        return redirect("import_books")

    elif request.method == "POST" and "clear_books" in request.POST:
        Book.objects.all().delete()
        messages.success(request, "All books have been deleted.")
        return redirect("import_books")

    return render(request, "books/import_books.html")
