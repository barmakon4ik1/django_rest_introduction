# Generated by Django 5.1 on 2024-08-19 09:11

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("newapp", "0005_genre_book_genres"),
    ]

    operations = [
        migrations.AddField(
            model_name="book",
            name="is_banned",
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name="book",
            name="genres",
            field=models.ManyToManyField(related_name="books", to="newapp.genre"),
        ),
    ]
