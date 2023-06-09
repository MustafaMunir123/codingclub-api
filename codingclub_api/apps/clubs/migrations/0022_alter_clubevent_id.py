# Generated by Django 4.1.2 on 2023-04-10 21:10

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):
    dependencies = [
        ("clubs", "0021_alter_clubevent_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="clubevent",
            name="id",
            field=models.UUIDField(
                default=uuid.uuid4, editable=False, primary_key=True, serialize=False
            ),
        ),
    ]
