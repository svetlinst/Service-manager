# Generated by Django 4.1.1 on 2023-04-24 13:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import service_manager.customers.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("main", "0021_servicerequest"),
    ]

    operations = [
        migrations.AddField(
            model_name="servicerequest",
            name="closed_on",
            field=models.DateTimeField(blank=True, null=True, verbose_name="closed on"),
        ),
        migrations.AddField(
            model_name="servicerequest",
            name="handled_on",
            field=models.DateTimeField(
                blank=True, null=True, verbose_name="handled on"
            ),
        ),
        migrations.AlterField(
            model_name="servicerequest",
            name="closed_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="closed_by",
                to=settings.AUTH_USER_MODEL,
                verbose_name="closed by",
            ),
        ),
        migrations.AlterField(
            model_name="servicerequest",
            name="handled_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="handled_by",
                to=settings.AUTH_USER_MODEL,
                verbose_name="handled by",
            ),
        ),
        migrations.AlterField(
            model_name="servicerequest",
            name="problem_description",
            field=models.CharField(max_length=255, verbose_name="problem description"),
        ),
        migrations.AlterField(
            model_name="servicerequest",
            name="requestor_name",
            field=models.CharField(max_length=100, verbose_name="requestor name"),
        ),
        migrations.AlterField(
            model_name="servicerequest",
            name="requestor_phone_number",
            field=models.CharField(
                max_length=20,
                validators=[
                    service_manager.customers.validators.phone_number_validator
                ],
                verbose_name="requestor phone number",
            ),
        ),
        migrations.AlterField(
            model_name="servicerequest",
            name="service_order",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="main.serviceorderheader",
                verbose_name="service order",
            ),
        ),
    ]
