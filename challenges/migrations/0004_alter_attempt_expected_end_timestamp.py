# Generated by Django 4.1 on 2022-08-05 12:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("challenges", "0003_alter_attempt_actual_end_timestamp_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="attempt",
            name="expected_end_timestamp",
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]