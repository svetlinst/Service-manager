# Generated by Django 4.1.1 on 2023-11-27 18:34

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("master_data", "0007_sla"),
    ]

    operations = [
        migrations.CreateModel(
            name="DeliveryRequest",
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
                ("created_on", models.DateTimeField(auto_now_add=True)),
                ("updated_on", models.DateTimeField(auto_now=True)),
                ("active", models.BooleanField(default=True)),
                ("quantity", models.FloatField(verbose_name="quantity")),
                (
                    "discount",
                    models.FloatField(
                        validators=[django.core.validators.MinValueValidator(0)],
                        verbose_name="discount",
                    ),
                ),
                (
                    "material",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="master_data.material",
                        verbose_name="material",
                    ),
                ),
            ],
            options={"abstract": False,},
        ),
    ]