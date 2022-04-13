# Generated by Django 4.0.3 on 2022-04-13 10:16

from django.db import migrations, models
import django.db.models.deletion
import football_app.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Nazwa ligi')),
                ('country', models.CharField(max_length=128, unique=True, verbose_name='Kraj rozgrywek')),
                ('teams_played', models.PositiveSmallIntegerField(validators=[football_app.validators.validate_teams_count], verbose_name='Liczba drużyn')),
                ('actuall_season', models.CharField(max_length=9, validators=[football_app.validators.validate_season], verbose_name='Sezon')),
            ],
            options={
                'verbose_name': 'Liga',
                'verbose_name_plural': 'Ligi',
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='Nazwa drużyny')),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='football_app.league', verbose_name='Liga')),
            ],
            options={
                'verbose_name': 'Drużyna',
                'verbose_name_plural': 'Drużyny',
            },
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_home_goals', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Bramki gospodarzy')),
                ('team_away_goals', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Bramki gości')),
                ('match_day', models.PositiveSmallIntegerField(verbose_name='Kolejka meczowa')),
                ('match_day_date', models.DateField(blank=True, null=True, verbose_name='Dzień meczowy')),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='football_app.league', verbose_name='Liga')),
                ('team_away', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='games_away', to='football_app.team', verbose_name='Drużyna gości')),
                ('team_home', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='games_home', to='football_app.team', verbose_name='Drużyna gospodarzy')),
            ],
            options={
                'verbose_name': 'Mecz',
                'verbose_name_plural': 'Mecze',
            },
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('season', models.CharField(max_length=9, validators=[football_app.validators.validate_season], verbose_name='Sezon')),
                ('points', models.SmallIntegerField(default=0, verbose_name='Liczba punktów')),
                ('matches_played', models.PositiveSmallIntegerField(default=0, verbose_name='Liczba meczy rozegranych')),
                ('goals_scored', models.PositiveSmallIntegerField(default=0, verbose_name='Bramki strzelone')),
                ('goals_lost', models.PositiveSmallIntegerField(default=0, verbose_name='Bramki stracone')),
                ('goals_balance', models.SmallIntegerField(default=0, verbose_name='Bilans bramkowy')),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='football_app.league', verbose_name='Liga')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='football_app.team', verbose_name='Drużyna')),
            ],
            options={
                'verbose_name': 'Poprzedni sezon',
                'verbose_name_plural': 'Poprzednie sezony',
                'unique_together': {('team', 'season')},
            },
        ),
    ]
