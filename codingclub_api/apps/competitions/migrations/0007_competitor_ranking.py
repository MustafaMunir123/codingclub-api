# Generated by Django 4.1.2 on 2023-04-18 23:58

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("competitions", "0006_alter_competition_id_alter_competitor_id"),
    ]

    operations = [
        migrations.AddField(
            model_name="competitor",
            name="ranking",
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
