# Generated by Django 5.1.4 on 2025-01-15 11:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("garden", "0005_alter_garden_user"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="gardenplant",
            name="notes",
        ),
    ]
