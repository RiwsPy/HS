# Generated by Django 3.2.9 on 2021-11-19 21:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0019_card_hidecost'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='bonus_value',
            field=models.IntegerField(null=True),
        ),
    ]
