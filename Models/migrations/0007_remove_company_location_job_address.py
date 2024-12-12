# Generated by Django 4.2.15 on 2024-12-12 09:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("Models", "0006_remove_job_location"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="company",
            name="location",
        ),
        migrations.AddField(
            model_name="job",
            name="address",
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
