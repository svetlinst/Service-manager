# Generated by Django 4.1.1 on 2023-11-27 10:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("customers", "0016_alter_customer_email_address"),
    ]

    operations = [
        migrations.AlterModelOptions(name="customer", options={"ordering": ("name",)},),
        migrations.AlterField(
            model_name="customerasset",
            name="inventory_number",
            field=models.CharField(
                blank=True, max_length=30, null=True, verbose_name="inventory_number"
            ),
        ),
        migrations.AlterField(
            model_name="customerasset",
            name="product_number",
            field=models.CharField(
                blank=True, max_length=30, null=True, verbose_name="product_number"
            ),
        ),
        migrations.AlterField(
            model_name="customerasset",
            name="serial_number",
            field=models.CharField(
                blank=True, max_length=30, null=True, verbose_name="serial_number"
            ),
        ),
    ]
