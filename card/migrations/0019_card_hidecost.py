# Generated by Django 3.2.9 on 2021-11-19 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0018_card_hidestats'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='hideCost',
            field=models.BooleanField(default=False),
        ),
    ]
