# Generated by Django 4.1.2 on 2023-04-02 22:47

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0019_remove_user_gender"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="user",
            name="groups",
        ),
        migrations.AddField(
            model_name="user",
            name="gender",
            field=models.CharField(
                choices=[("Male", "Male"), ("Female", "Female"), ("Other", "Other")],
                default="Male",
                max_length=10,
            ),
            preserve_default=False,
        ),
    ]
