# Generated by Django 3.2.9 on 2021-11-19 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0010_auto_20211119_2159'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='targetingArrowText',
            field=models.CharField(default='', max_length=255),
        ),
    ]