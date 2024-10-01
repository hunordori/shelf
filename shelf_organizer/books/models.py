from django.db import models

class Book(models.Model):
    mms_id = models.CharField(max_length=50)
    title = models.CharField(max_length=255)
    library_name = models.CharField(max_length=255)
    process_type = models.CharField(max_length=100)
    barcode = models.CharField(max_length=100, unique=True)
    call_number = models.CharField(max_length=100)

    def __str__(self):
        return self.title