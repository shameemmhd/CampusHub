# Generated by Django 4.1.4 on 2024-05-18 09:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Myapplication', '0004_book_bookpost_exchangerequest'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='department',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, null=True),
        ),
    ]
