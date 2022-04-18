from django.db import models
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django_countries.fields import CountryField

from .managers import CustomUserManager
from .validators import validate_teams_count

# Create your models here.


class User(AbstractUser):

    username = None
    first_name = models.CharField(verbose_name='Imię', max_length=64)
    last_name = models.CharField(verbose_name='Nazwisko', max_length=64)
    email = models.EmailField(verbose_name='Email', max_length=255, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name = _('Użytkownik')
        verbose_name_plural = _('Użytkownicy')

    def __str__(self):
        return self.first_name + " " + self.last_name

class League(models.Model):

    class Meta:
        verbose_name = "Liga"
        verbose_name_plural = "Ligi"

    name = models.CharField(max_length=128, verbose_name="Nazwa ligi")
    country = CountryField(verbose_name="Kraj rozgrywek", blank_label="Wybierz z listy")
    teams_played = models.PositiveSmallIntegerField(verbose_name="Liczba drużyn", validators=[validate_teams_count])

    def __str__(self):
        return self.name


class Team(models.Model):

    class Meta:
        verbose_name = "Drużyna"
        verbose_name_plural = "Drużyny"

    actuall_league = models.ForeignKey("League", related_name="teams", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Aktualna liga")
    actuall_season = models.ForeignKey("Season", related_name="teams", on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Aktualny sezon")
    name = models.CharField(max_length=128, unique=True, verbose_name="Nazwa drużyny")
    country = CountryField(verbose_name="Kraj rozgrywek", blank_label="Wybierz z listy")

    def clean(self, *args, **kwargs):
        
        super().clean(*args, **kwargs)
    
        teams_count = self.__class__._default_manager.filter(
            actuall_league=self.actuall_league,
        ).count()
        
        if teams_count >= self.actuall_league.teams_played:
            raise ValidationError({"actuall_league": "Liga już ma komplet drużyn"})
        
    def __str__(self):
        return self.name


class Season(models.Model):
    
    class Meta:
        verbose_name = "Sezon"
        verbose_name_plural = "Sezony"

    league = models.ForeignKey("League", related_name="seasons", on_delete=models.CASCADE, verbose_name="Liga")
    date_start = models.DateField(verbose_name="Data rozpoczęcia")
    season_years = models.CharField(max_length=9, verbose_name="Sezon")
    season_table = models.ManyToManyField('Team', related_name='seasons', through='SeasonTable')

    def save(self, *args, **kwargs):

        year = self.date_start.year
        self.season_years = str(year) + "/" + str(year + 1)

        season = self.__class__._default_manager.filter(
            league=self.league,
            season_years=self.season_years
        ).first()

        if season:
            raise ValidationError({NON_FIELD_ERRORS: "Sezon już ujęty w bazie"})

        super().save(*args, **kwargs)

    def __str__(self):
        return self.league.name + " sezon " + self.season_years


class SeasonTable(models.Model):
    
    class Meta:
        unique_together = ('team', 'season')
        verbose_name = "Tabela ligowa"
        verbose_name_plural = "Tabela ligowa"

    season = models.ForeignKey("Season", related_name="season_tables", on_delete=models.CASCADE, verbose_name="Sezon")
    team = models.ForeignKey("Team", related_name="season_tables", on_delete=models.CASCADE, verbose_name="Drużyna")
    points = models.SmallIntegerField(default=0, verbose_name="Liczba punktów")
    matches_played = models.PositiveSmallIntegerField(default=0, verbose_name="Liczba meczy rozegranych")
    goals_scored = models.PositiveSmallIntegerField(default=0, verbose_name="Bramki strzelone")
    goals_lost = models.PositiveSmallIntegerField(default=0, verbose_name="Bramki stracone")
    goals_balance = models.SmallIntegerField(default=0, verbose_name="Bilans bramkowy")
    
    def save(self, *args, **kwargs):
        
        self.goals_balance = self.goals_scored - self.goals_lost
        
        super().save(*args, **kwargs)


class Game(models.Model):
    
    class Meta:
        verbose_name = "Mecz"
        verbose_name_plural = "Mecze"
    
    season = models.ForeignKey("Season", related_name="games", on_delete=models.CASCADE, verbose_name="Sezon")
    team_home = models.ForeignKey("Team", related_name="games_home", on_delete=models.CASCADE, verbose_name="Drużyna gospodarzy")
    team_away = models.ForeignKey("Team", related_name="games_away", on_delete=models.CASCADE, verbose_name="Drużyna gości")
    team_home_goals = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Bramki gospodarzy")
    team_away_goals = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Bramki gości")
    match_day = models.PositiveSmallIntegerField(verbose_name="Kolejka meczowa")
    match_day_date = models.DateField(null=True, blank=True, verbose_name="Dzień meczowy")

    def save(self, *args, **kwargs):
        
        game = self.__class__._default_manager.filter(
            team_home=self.team_home,
            team_away=self.team_away,
            season=self.season
        ).first()

        if game:
            raise ValidationError({NON_FIELD_ERRORS: "Mecz już ujęty w terminarzu"})

        super().save(*args, **kwargs)
