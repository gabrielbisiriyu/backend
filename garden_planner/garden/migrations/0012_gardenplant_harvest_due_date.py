# Generated by Django 5.1.4 on 2025-01-23 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("garden", "0011_remove_plant_fertilizer_instructions_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="gardenplant",
            name="harvest_due_date",
            field=models.DateField(blank=True, null=True),
        ),
    ]
