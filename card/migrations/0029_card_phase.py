# Generated by Django 3.2.9 on 2021-11-19 21:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0028_card_zone_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='phase',
            field=models.CharField(max_length=255, null=True),
        ),
    ]