# Generated by Django 5.2 on 2025-04-29 13:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("codes", "0004_doctor_password"),
    ]

    operations = [
        migrations.AddField(
            model_name="appointment",
            name="is_approved",
            field=models.BooleanField(default=False),
        ),
    ]
