# Generated by Django 4.1.2 on 2023-03-31 22:14

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0013_alter_club_user"),
    ]

    operations = [
        migrations.AlterField(
            model_name="clubmember",
            name="club",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="club",
                to="users.club",
            ),
        ),
        migrations.AlterField(
            model_name="clubmember",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="user",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
