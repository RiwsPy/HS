# Generated by Django 3.2.9 on 2021-12-04 16:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0005_alter_card_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='race',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='card.race'),
        ),
        migrations.AlterField(
            model_name='card',
            name='type',
            field=models.CharField(default='DEFAULT', max_length=30),
        ),
    ]
