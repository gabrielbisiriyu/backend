# Generated by Django 5.1.4 on 2025-01-23 17:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("garden", "0010_remove_plant_harvest_date_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="plant",
            name="fertilizer_instructions",
        ),
        migrations.RemoveField(
            model_name="plant",
            name="pruning_instructions",
        ),
    ]
