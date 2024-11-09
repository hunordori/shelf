from django.db import models


class Book(models.Model):
    title = models.CharField(max_length=255)
    barcode = models.CharField(max_length=100, unique=True)
    call_number = models.CharField(max_length=100)

    def __str__(self):
        return self.title
