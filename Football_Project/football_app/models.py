from django.db import models
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS

from .validators import validate_season, validate_teams_count

# Create your models here.


class League(models.Model):

    class Meta:
        verbose_name = "Liga"
        verbose_name_plural = "Ligi"

    name = models.CharField(max_length=128, verbose_name="Nazwa ligi")
    country = models.CharField(max_length=128, unique=True, verbose_name="Kraj rozgrywek")
    teams_played = models.PositiveSmallIntegerField(verbose_name="Liczba drużyn", validators=[validate_teams_count])
    actuall_season = models.CharField(max_length=9, verbose_name="Sezon", validators=[validate_season])

    def __str__(self):
        return self.name


class Team(models.Model):

    class Meta:
        verbose_name = "Drużyna"
        verbose_name_plural = "Drużyny"

    league = models.ForeignKey("League", on_delete=models.CASCADE, verbose_name="Liga")
    name = models.CharField(max_length=128, unique=True, verbose_name="Nazwa drużyny")

    def __str__(self):
        return self.name


class Game(models.Model):
    
    class Meta:
        verbose_name = "Mecz"
        verbose_name_plural = "Mecze"
    
    league = models.ForeignKey("League", on_delete=models.CASCADE, verbose_name="Liga")
    team_home = models.ForeignKey("Team", related_name="games_home", on_delete=models.CASCADE, verbose_name="Drużyna gospodarzy")
    team_home_goals = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Bramki gospodarzy")
    team_away = models.ForeignKey("Team", related_name="games_away", on_delete=models.CASCADE, verbose_name="Drużyna gości")
    team_away_goals = models.PositiveSmallIntegerField(null=True, blank=True, verbose_name="Bramki gości")
    match_day = models.PositiveSmallIntegerField(verbose_name="Kolejka meczowa")
    match_day_date = models.DateField(null=True, blank=True, verbose_name="Dzień meczowy")

    def save(self, *args, **kwargs):
        
        game = self.__class__._default_manager.filter(
            match_day=self.match_day,
            team_home=self.team_home
        ).first()

        if game:
            raise ValidationError({NON_FIELD_ERRORS: "Kolejka już ujęta w terminarzu"})
        
        game = self.__class__._default_manager.filter(
            team_home=self.team_home,
            team_away=self.team_away
        ).first()

        if game:
            raise ValidationError({NON_FIELD_ERRORS: "Mecz już ujęty w terminarzu"})

        super().save(*args, **kwargs)


class Season(models.Model):
    
    class Meta:
        unique_together = ('team', 'season')
        verbose_name = "Poprzedni sezon"
        verbose_name_plural = "Poprzednie sezony"

    league = models.ForeignKey("League", on_delete=models.CASCADE, verbose_name="Liga")
    team = models.ForeignKey("Team", on_delete=models.CASCADE, verbose_name="Drużyna")
    season = models.CharField(max_length=9, verbose_name="Sezon", validators=[validate_season])
    points = models.SmallIntegerField(default=0, verbose_name="Liczba punktów")
    matches_played = models.PositiveSmallIntegerField(default=0, verbose_name="Liczba meczy rozegranych")
    goals_scored = models.PositiveSmallIntegerField(default=0, verbose_name="Bramki strzelone")
    goals_lost = models.PositiveSmallIntegerField(default=0, verbose_name="Bramki stracone")
    goals_balance = models.SmallIntegerField(default=0, verbose_name="Bilans bramkowy")
    
    def save(self, *args, **kwargs):
        
        self.goals_balance = self.goals_scored - self.goals_lost
        
        super().save(*args, **kwargs)

    def __str__(self):
        return self.team + " " + self.season
