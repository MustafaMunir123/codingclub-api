# Generated by Django 4.1.2 on 2023-04-10 21:28

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("clubs", "0023_alter_clubevent_end_date_alter_clubevent_start_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="clubevent",
            name="end_date",
            field=models.DateField(default="2023-3-4"),
        ),
        migrations.AlterField(
            model_name="clubevent",
            name="start_date",
            field=models.DateField(default="2023-3-4"),
        ),
    ]