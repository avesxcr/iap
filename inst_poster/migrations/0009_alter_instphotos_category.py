# Generated by Django 5.0.1 on 2024-01-25 16:04

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inst_poster', '0008_category_remove_datacredentials_timestampp_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='instphotos',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='inst_poster.category'),
        ),
    ]
