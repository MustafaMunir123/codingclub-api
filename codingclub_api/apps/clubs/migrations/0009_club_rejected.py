# Generated by Django 4.1.2 on 2023-04-04 01:04

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("clubs", "0008_club_is_accepted"),
    ]

    operations = [
        migrations.AddField(
            model_name="club",
            name="rejected",
            field=models.BooleanField(default=False, null=True),
        ),
    ]