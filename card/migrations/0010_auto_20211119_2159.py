# Generated by Django 3.2.9 on 2021-11-19 20:59

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0009_auto_20211119_2158'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='mechanics',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255, null=True), default=list, size=None),
        ),
        migrations.AlterField(
            model_name='card',
            name='referencedTags',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=255, null=True), default=list, size=None),
        ),
    ]