# Generated by Django 3.2.9 on 2021-11-20 11:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0033_auto_20211120_1231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='duration',
            field=models.SmallIntegerField(null=True),
        ),
    ]
