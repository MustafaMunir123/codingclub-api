# Generated by Django 4.1.2 on 2023-03-28 23:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0004_alter_category_tags_clubrule"),
    ]

    operations = [
        migrations.AddField(
            model_name="club",
            name="logo",
            field=models.ImageField(default=1, upload_to="clubs/logo"),
            preserve_default=False,
        ),
    ]