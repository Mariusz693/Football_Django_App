# Generated by Django 4.0.3 on 2022-04-29 16:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('football_app', '0003_alter_season_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='game',
            options={'ordering': ['match_day'], 'verbose_name': 'Mecz', 'verbose_name_plural': 'Mecze'},
        ),
    ]
