# Generated by Django 4.1.1 on 2022-09-15 05:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0018_serviceorderheader_customer_asset'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='serviceorderheader',
            name='accepted_by',
        ),
    ]
