# Generated by Django 4.1.2 on 2023-03-28 22:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0002_clubmember"),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "tags",
                    models.CharField(
                        choices=[
                            ("1", "AI"),
                            ("2", "Data Science"),
                            ("3", "Web Engineering"),
                            ("4", "Cloud"),
                            ("5", "Cyber Security"),
                            ("6", "Hardware"),
                            ("7", "Machine Learning"),
                            ("8", "Robotics"),
                        ],
                        max_length=40,
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="club",
            name="category",
            field=models.ManyToManyField(related_name="category", to="users.category"),
        ),
    ]
