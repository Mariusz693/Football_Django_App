# Generated by Django 4.0.3 on 2022-04-20 16:04

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import django_countries.fields
import football_app.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Nazwa ligi')),
                ('country', django_countries.fields.CountryField(max_length=2, verbose_name='Kraj rozgrywek')),
                ('teams_played', models.PositiveSmallIntegerField(validators=[football_app.validators.validate_teams_count], verbose_name='Liczba drużyn')),
            ],
            options={
                'verbose_name': 'Liga',
                'verbose_name_plural': 'Ligi',
            },
        ),
        migrations.CreateModel(
            name='Season',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_start', models.DateField(verbose_name='Data rozpoczęcia')),
                ('date_end', models.DateField(null=True, verbose_name='Data zakończenia')),
                ('season_years', models.CharField(max_length=9, verbose_name='Sezon')),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='seasons', to='football_app.league', verbose_name='Liga')),
            ],
            options={
                'verbose_name': 'Sezon',
                'verbose_name_plural': 'Sezony',
            },
        ),
        migrations.CreateModel(
            name='Team',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, unique=True, verbose_name='Nazwa drużyny')),
                ('country', django_countries.fields.CountryField(max_length=2, verbose_name='Kraj rozgrywek')),
                ('actuall_league', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='teams', to='football_app.league', verbose_name='Aktualna liga')),
                ('actuall_season', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='teams', to='football_app.season', verbose_name='Aktualny sezon')),
            ],
            options={
                'verbose_name': 'Drużyna',
                'verbose_name_plural': 'Drużyny',
            },
        ),
        migrations.CreateModel(
            name='SeasonTable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('points', models.SmallIntegerField(default=0, verbose_name='Liczba punktów')),
                ('matches_played', models.PositiveSmallIntegerField(default=0, verbose_name='Liczba meczy rozegranych')),
                ('goals_scored', models.PositiveSmallIntegerField(default=0, verbose_name='Bramki strzelone')),
                ('goals_lost', models.PositiveSmallIntegerField(default=0, verbose_name='Bramki stracone')),
                ('goals_balance', models.SmallIntegerField(default=0, verbose_name='Bilans bramkowy')),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='season_tables', to='football_app.season', verbose_name='Sezon')),
                ('team', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='season_tables', to='football_app.team', verbose_name='Drużyna')),
            ],
            options={
                'verbose_name': 'Tabela ligowa',
                'verbose_name_plural': 'Tabela ligowa',
                'ordering': ['points', 'goals_balance'],
                'unique_together': {('team', 'season')},
            },
        ),
        migrations.AddField(
            model_name='season',
            name='season_table',
            field=models.ManyToManyField(related_name='seasons', through='football_app.SeasonTable', to='football_app.team'),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('first_name', models.CharField(max_length=64, verbose_name='Imię')),
                ('last_name', models.CharField(max_length=64, verbose_name='Nazwisko')),
                ('email', models.EmailField(max_length=255, unique=True, verbose_name='Email')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Użytkownik',
                'verbose_name_plural': 'Użytkownicy',
            },
        ),
        migrations.AlterUniqueTogether(
            name='season',
            unique_together={('league', 'season_years')},
        ),
        migrations.CreateModel(
            name='Game',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('team_home_goals', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Bramki gospodarzy')),
                ('team_away_goals', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Bramki gości')),
                ('match_day', models.PositiveSmallIntegerField(blank=True, null=True, verbose_name='Kolejka meczowa')),
                ('match_day_date', models.DateField(blank=True, null=True, verbose_name='Dzień meczowy')),
                ('season', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='games', to='football_app.season', verbose_name='Sezon')),
                ('team_away', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='games_away', to='football_app.team', verbose_name='Drużyna gości')),
                ('team_home', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='games_home', to='football_app.team', verbose_name='Drużyna gospodarzy')),
            ],
            options={
                'verbose_name': 'Mecz',
                'verbose_name_plural': 'Mecze',
                'unique_together': {('season', 'team_home', 'team_away')},
            },
        ),
    ]
