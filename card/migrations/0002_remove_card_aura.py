# Generated by Django 3.2.9 on 2021-11-23 18:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='aura',
        ),
    ]
