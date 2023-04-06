# Generated by Django 4.1.2 on 2023-04-06 17:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("clubs", "0013_alter_clubevent_end_date_alter_clubevent_going_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="clubevent",
            name="club",
        ),
        migrations.RemoveField(
            model_name="clubevent",
            name="going",
        ),
        migrations.AddField(
            model_name="clubevent",
            name="of_club",
            field=models.ForeignKey(
                default="994f9131-12bd-43cf-a95e-3af7fb9fee8e",
                on_delete=django.db.models.deletion.CASCADE,
                related_name="of_club",
                to="clubs.club",
            ),
            preserve_default=False,
        ),
        migrations.CreateModel(
            name="EventGoing",
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
                    "event",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="event",
                        to="clubs.clubevent",
                    ),
                ),
                (
                    "going",
                    models.ManyToManyField(
                        related_name="going", to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
        ),
    ]
