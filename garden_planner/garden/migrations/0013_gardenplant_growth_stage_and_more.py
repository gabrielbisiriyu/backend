# Generated by Django 5.1.4 on 2025-01-24 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("garden", "0012_gardenplant_harvest_due_date"),
    ]

    operations = [
        migrations.AddField(
            model_name="gardenplant",
            name="growth_stage",
            field=models.CharField(
                blank=True,
                choices=[
                    ("SEEDLING", "Seedling"),
                    ("VEGETATIVE", "Vegetative"),
                    ("FLOWERING", "Flowering"),
                    ("FRUITING", "Fruiting"),
                ],
                max_length=50,
                null=True,
            ),
        ),
        migrations.AddField(
            model_name="gardenplant",
            name="maintenance_completed",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="notification",
            name="task_type",
            field=models.CharField(
                blank=True,
                choices=[("WATERING", "Watering"), ("MAINTENANCE", "Maintenance")],
                max_length=20,
                null=True,
            ),
        ),
    ]
