# Generated by Django 4.1.2 on 2023-03-28 23:10

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0005_club_logo"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="category",
            options={"verbose_name_plural": "Categories"},
        ),
    ]
