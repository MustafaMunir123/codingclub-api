# Generated by Django 4.1.2 on 2023-04-08 17:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("clubs", "0016_alter_category_tags"),
    ]

    operations = [
        migrations.AlterField(
            model_name="clubdomain",
            name="domain",
            field=models.CharField(max_length=40, unique=True),
        ),
        migrations.AlterField(
            model_name="clubrole",
            name="role",
            field=models.CharField(max_length=40, unique=True),
        ),
    ]
