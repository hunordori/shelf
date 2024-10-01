import os
import pandas as pd
from django.core.management.base import BaseCommand
from books.models import Book

class Command(BaseCommand):
    help = 'Import book data from CSV file'

    def handle(self, *args, **kwargs):
        # Define the path to the CSV file (relative to the project root)
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
        file_path = os.path.join(base_dir, 'data', 'current_inventory.csv')

        # Read CSV file
        df = pd.read_csv(file_path)

        # Iterate over rows and create Book objects
        for _, row in df.iterrows():
            book, created = Book.objects.get_or_create(
                barcode=row['Barcode'],
                defaults={
                    'mms_id': row['MMS Id'],
                    'title': row['Title'],
                    'library_name': row['Library Name (Active)'],
                    'process_type': row['Process Type'],
                    'call_number': row['Call Number'],
                }
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully imported book data from {file_path}!'))
