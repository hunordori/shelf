# Generated by Django 5.1.1 on 2024-10-01 00:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mms_id', models.CharField(max_length=50)),
                ('title', models.CharField(max_length=255)),
                ('library_name', models.CharField(max_length=255)),
                ('process_type', models.CharField(max_length=100)),
                ('barcode', models.CharField(max_length=100, unique=True)),
                ('call_number', models.CharField(max_length=100)),
            ],
        ),
    ]
