# Generated by Django 3.2.9 on 2021-11-19 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0011_card_targetingarrowtext'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='elite',
            field=models.BooleanField(default=False, max_length=255),
        ),
    ]
