# Generated by Django 3.2.9 on 2021-12-05 13:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0006_auto_20211204_1730'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='synergy',
            field=models.CharField(choices=[('ALL', 'ALL'), ('NONE', 'NONE'), ('BEAST', 'BEAST'), ('DEMON', 'DEMON'), ('MECHANICAL', 'MECHANICAL'), ('MURLOC', 'MURLOC'), ('DRAGON', 'DRAGON'), ('PIRATE', 'PIRATE'), ('ELEMENTAL', 'ELEMENTAL'), ('QUILBOAR', 'QUILBOAR')], default='NONE', max_length=30),
        ),
    ]
