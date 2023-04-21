# Generated by Django 4.1.2 on 2023-04-18 21:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("clubs", "0030_rename_registration_left_clubevent_registrations_made"),
    ]

    operations = [
        migrations.AlterField(
            model_name="clubevent",
            name="registrations_made",
            field=models.IntegerField(
                default=0,
                help_text="No of registrations that have been made i.e. 32/40",
            ),
        ),
    ]