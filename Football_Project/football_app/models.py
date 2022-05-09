from django.db import models
from django.contrib.auth.models import AbstractUser
from django_countries.fields import CountryField

from .managers import CustomUserManager
from .validators import validate_teams_count, validate_competition_class

# Create your models here.


class User(AbstractUser):

    class Meta:
            verbose_name = 'Użytkownik'
            verbose_name_plural = 'Użytkownicy'

    username = None
    first_name = models.CharField(verbose_name='Imię', max_length=64)
    last_name = models.CharField(verbose_name='Nazwisko', max_length=64)
    email = models.EmailField(verbose_name='Email', max_length=255, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.first_name + " " + self.last_name


class League(models.Model):

    class Meta:
        verbose_name = "Liga"
        verbose_name_plural = "Ligi"
        unique_together = ["competition_class", "country"]
        ordering = ["competition_class", "name"]

    name = models.CharField(max_length=128, verbose_name="Nazwa ligi")
    country = CountryField(blank_label="Wybierz z listy", verbose_name="Kraj rozgrywek")
    competition_class = models.PositiveSmallIntegerField(validators=[validate_competition_class], verbose_name="Klasa rozrywek")
    
    def __str__(self):
        return self.name

    def unique_error_message(self, model_class, unique_check):
        
        if unique_check == ("competition_class", "country"):
            return "W wybranym kraju istnieje już ta klasa rozgrywek"
        
        else:
            return super().unique_error_message(model_class, unique_check)


class Team(models.Model):

    class Meta:
        verbose_name = "Drużyna"
        verbose_name_plural = "Drużyny"
        ordering = ["name"]

    name = models.CharField(max_length=128, unique=True, error_messages={"unique": "Istnieje już drużyna o tej nazwie"}, verbose_name="Nazwa drużyny")
    country = CountryField(blank_label="Wybierz z listy", verbose_name="Kraj rozgrywek")       
    team_seasons = models.ManyToManyField('Season', related_name='teams', through='SeasonTeam', verbose_name="Sezony")

    def __str__(self):
        return self.name


class Season(models.Model):
    
    class Meta:
        verbose_name = "Sezon"
        verbose_name_plural = "Sezony"
        unique_together = ["league", "season_years"]
        ordering = ["-date_start"]

    league = models.ForeignKey("League", related_name="seasons", on_delete=models.CASCADE, verbose_name="Liga")
    season_years = models.CharField(max_length=9, verbose_name="Sezon")
    date_start = models.DateField(verbose_name="Data rozpoczęcia")
    date_end = models.DateField(null=True, blank=True, verbose_name="Data zakończenia")
    is_active = models.BooleanField(default=True, verbose_name="Aktualny")
    number_of_teams = models.PositiveSmallIntegerField(validators=[validate_teams_count], verbose_name="Liczba drużyn")
    season_teams = models.ManyToManyField('Team', related_name='seasons', through='SeasonTeam', verbose_name="Drużyny")

    def save(self, *args, **kwargs):
        
        year = self.date_start.year
        self.season_years = str(year) + "/" + str(year + 1)

        super().save(*args, **kwargs)

    def __str__(self):
        return self.league.name + " " + self.season_years

    def unique_error_message(self, model_class, unique_check):
        
        if unique_check == ("league", "season_years"):
            return "Liga posiada już sezon zapisany na ten rok"
        
        else:
            return super().unique_error_message(model_class, unique_check)


class SeasonTeam(models.Model):
    
    class Meta:
        verbose_name = "Tabela drużyny"
        verbose_name_plural = "Tabela drużyny"
        unique_together = ["team", "season"]
        ordering = ["-points", "-goals_balance"]

    season = models.ForeignKey("Season", related_name='season_team_table', on_delete=models.CASCADE, verbose_name="Sezon")
    team = models.ForeignKey("Team", related_name='season_team_table', on_delete=models.CASCADE, verbose_name="Drużyna")
    points = models.SmallIntegerField(default=0, verbose_name="Liczba punktów")
    matches_played = models.PositiveSmallIntegerField(default=0, verbose_name="Liczba meczy rozegranych")
    goals_scored = models.PositiveSmallIntegerField(default=0, verbose_name="Bramki strzelone")
    goals_lost = models.PositiveSmallIntegerField(default=0, verbose_name="Bramki stracone")
    goals_balance = models.SmallIntegerField(default=0, verbose_name="Bilans bramkowy")
    
    def save(self, *args, **kwargs):
        
        self.goals_balance = self.goals_scored - self.goals_lost
        
        super().save(*args, **kwargs)

    def unique_error_message(self, model_class, unique_check):
        
        if unique_check == ("team", "season"):
            return "Drużyna jest już przypisana do tego sezonu"
        
        else:
            return super().unique_error_message(model_class, unique_check)


class Game(models.Model):
    
    class Meta:
        verbose_name = "Mecz"
        verbose_name_plural = "Mecze"
        unique_together = ["season", "team_home", "team_away"]
        ordering = ["match_day", "-team_home"]
    
    season = models.ForeignKey("Season", related_name="games", on_delete=models.CASCADE, verbose_name="Sezon")
    team_home = models.ForeignKey("Team", related_name="games_home", on_delete=models.CASCADE, verbose_name="Drużyna gospodarzy")
    team_away = models.ForeignKey("Team", related_name="games_away", on_delete=models.CASCADE, verbose_name="Drużyna gości")
    team_home_goals = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Bramki gospodarzy")
    team_away_goals = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Bramki gości")
    match_day = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Kolejka meczowa")
    match_day_date = models.DateField(null=True, blank=True, verbose_name="Dzień meczowy")

    def unique_error_message(self, model_class, unique_check):
        
        if unique_check == ("season", "team_home", "team_away"):
            return "Ten mecz już został zapisany"
        
        else:
            return super().unique_error_message(model_class, unique_check)
