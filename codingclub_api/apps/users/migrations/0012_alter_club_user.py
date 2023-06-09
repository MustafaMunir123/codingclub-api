# Generated by Django 4.1.2 on 2023-03-31 00:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0011_alter_clubevent_club_alter_clubrule_club"),
    ]

    operations = [
        migrations.AlterField(
            model_name="club",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.DO_NOTHING,
                related_name="lead_user",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
