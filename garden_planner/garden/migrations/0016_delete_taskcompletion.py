# Generated by Django 5.1.4 on 2025-01-24 17:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("garden", "0015_taskcompletion"),
    ]

    operations = [
        migrations.DeleteModel(
            name="TaskCompletion",
        ),
    ]
