# Generated by Django 3.2.9 on 2021-12-05 17:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0008_alter_race_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rarity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.AlterField(
            model_name='race',
            name='name',
            field=models.CharField(max_length=30, primary_key=True, serialize=False),
        ),
    ]
