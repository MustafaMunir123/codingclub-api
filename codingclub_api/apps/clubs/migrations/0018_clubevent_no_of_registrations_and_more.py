# Generated by Django 4.1.2 on 2023-04-10 20:20

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("clubs", "0017_alter_clubdomain_domain_alter_clubrole_role"),
    ]

    operations = [
        migrations.AddField(
            model_name="clubevent",
            name="no_of_registrations",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="clubevent",
            name="registration_left",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="clubevent",
            name="registration_status",
            field=models.CharField(
                choices=[
                    ("Ongoing", "Ongoing"),
                    ("Up-Coming", "UP-Coming"),
                    ("Past", "Past"),
                ],
                default="UP-Coming",
                max_length=20,
            ),
        ),
        migrations.DeleteModel(
            name="EventGoing",
        ),
    ]
