# Generated by Django 3.2.9 on 2021-11-19 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='card',
            name='power_id',
        ),
        migrations.AddField(
            model_name='card',
            name='enchantment_dbfId',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='card',
            name='power_dbfId',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='card',
            name='repop_dbfId',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='card',
            name='battlegroundsNormalDbfId',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='card',
            name='battlegroundsPremiumDbfId',
            field=models.IntegerField(default=0),
        ),
    ]