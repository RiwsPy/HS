# Generated by Django 3.2.9 on 2021-11-19 21:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0023_card_hero_script'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='collectionText',
            field=models.CharField(default='', max_length=255),
        ),
    ]