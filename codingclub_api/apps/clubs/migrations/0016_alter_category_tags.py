# Generated by Django 4.1.2 on 2023-04-08 17:21

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("clubs", "0015_alter_clubrole_role"),
    ]

    operations = [
        migrations.AlterField(
            model_name="category",
            name="tags",
            field=models.CharField(max_length=40, unique=True),
        ),
    ]
