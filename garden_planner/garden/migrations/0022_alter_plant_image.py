# Generated by Django 5.1.4 on 2025-02-04 19:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("garden", "0021_alter_plant_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="plant",
            name="image",
            field=models.ImageField(blank=True, null=True, upload_to="images"),
        ),
    ]
