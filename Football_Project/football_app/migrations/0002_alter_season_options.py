# Generated by Django 4.0.3 on 2022-04-24 17:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('football_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='season',
            options={'ordering': ['date_start'], 'verbose_name': 'Sezon', 'verbose_name_plural': 'Sezony'},
        ),
    ]
