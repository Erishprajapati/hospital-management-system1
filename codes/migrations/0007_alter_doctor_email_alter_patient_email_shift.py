# Generated by Django 5.2 on 2025-05-02 17:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("codes", "0006_patient_user_alter_appointment_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="doctor",
            name="email",
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.AlterField(
            model_name="patient",
            name="email",
            field=models.EmailField(max_length=254, unique=True),
        ),
        migrations.CreateModel(
            name="shift",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("Date", models.DateField()),
                ("start_time", models.TimeField()),
                ("end_time", models.TimeField()),
                (
                    "doctor",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="codes.doctor"
                    ),
                ),
            ],
        ),
    ]
