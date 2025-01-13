# Generated by Django 5.1.4 on 2025-01-13 12:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("garden", "0004_alter_garden_user"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name="garden",
            name="user",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="gardens",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
