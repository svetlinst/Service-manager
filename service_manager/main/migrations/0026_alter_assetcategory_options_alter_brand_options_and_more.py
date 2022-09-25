# Generated by Django 4.1.1 on 2022-09-25 22:09

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0025_rename_serviceordernode_serviceordernote'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='assetcategory',
            options={'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='brand',
            options={'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='customerasset',
            options={'ordering': ('asset__category__name', 'asset__brand__name', 'asset__model_name', 'serial_number')},
        ),
        migrations.AlterModelOptions(
            name='customerdepartment',
            options={'ordering': ('name',)},
        ),
        migrations.AlterModelOptions(
            name='customerrepresentative',
            options={'ordering': ('first_name', 'last_name')},
        ),
        migrations.AlterModelOptions(
            name='serviceordernote',
            options={'ordering': ('-created_on',)},
        ),
        migrations.RemoveField(
            model_name='serviceorderheader',
            name='customer_representative',
        ),
        migrations.AddField(
            model_name='serviceorderheader',
            name='handed_over_by',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='handed_by_customer_representative', to='main.customerrepresentative'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='serviceorderheader',
            name='handed_over_to',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='handed_to_customer_representative', to='main.customerrepresentative'),
        ),
        migrations.AlterField(
            model_name='customerrepresentative',
            name='email_address',
            field=models.CharField(blank=True, max_length=254, null=True, validators=[django.core.validators.EmailValidator]),
        ),
    ]
