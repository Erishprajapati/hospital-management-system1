# Generated by Django 5.2 on 2025-04-29 02:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("codes", "0002_alter_patient_emergency_contact"),
    ]

    operations = [
        migrations.AddField(
            model_name="patient",
            name="password",
            field=models.CharField(default=11, max_length=100),
            preserve_default=False,
        ),
    ]
