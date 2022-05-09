from django.core.exceptions import ValidationError
from .models import Game
from random import shuffle
from datetime import timedelta


def create_season(season):
    
    teams = season.teams.all()
    teams = list(teams)
    number_of_teams = len(teams)
    if number_of_teams % 2 == 1:
        raise ValidationError("Liczba drużyn musi być parzysta")
    
    # Create table
    
    games = []
        
    for i in range(1, number_of_teams):
        games.append([])
        for j in range(int(number_of_teams / 2)):
            games[i-1].append([])
            games[i-1][j]=["", ""]
    
    # Supplement the table
    
    for i in range(1, number_of_teams):    
        if i <= int(number_of_teams / 2):
            games[2*i-2][0][0] = i - 1
            games[2*i-2][0][1] = number_of_teams - 1
            w = 2*i-2
        else:
            games[2*i-1-number_of_teams][0][1] = i - 1
            games[2*i-1-number_of_teams][0][0] = number_of_teams - 1
            w = 2*i-1-number_of_teams
        j = i + 1
        for k in range(1, number_of_teams - 1):
            if j >= number_of_teams:
                j=1
            if k <= (number_of_teams - 2) / 2:
                games[w][k][0] = j - 1
            else:
                games[w][number_of_teams-1-k][1] = j - 1
            j += 1

    # Create timetable

    shuffle(teams)
    day_start = season.date_start
    if day_start.weekday() != 6:
        match_day_date = day_start + timedelta(days=(6-day_start.weekday()))

    for i in range(1, number_of_teams * 2 - 1):  
        if i < number_of_teams:
            j = i - 1
            for k in range(int(number_of_teams / 2)):
                Game.objects.create(
                    season=season,
                    match_day=i,
                    match_day_date=match_day_date,
                    team_home=teams[games[j][k][0]],
                    team_away=teams[games[j][k][1]]
                )
        else:
            j = i - number_of_teams
            for k in range(int(number_of_teams / 2)):
                Game.objects.create(
                    season=season,
                    match_day=i,
                    match_day_date=match_day_date,
                    team_home=teams[games[j][k][1]],
                    team_away=teams[games[j][k][0]]
                )
        match_day_date = match_day_date + timedelta(days=7)
    
    # Check timetable

    games = Game.objects.filter(season=season)
    number_to_check = number_of_teams / 2 * (number_of_teams - 1) * 2
    if number_to_check != games.count():
        season.delete()
        raise ValidationError("Błąd tworzenia sezonu i terminarza")
    else:
        season.date_end = games.last().match_day_date
        season.save()


def calculate_points(data):
    
    game = Game.objects.filter(pk=data["pk"]).first()
    if game and game.team_home_goals is None:
        season = game.season
        try:
            game.team_home_goals = int(data["team_home_goals"])
            game.team_away_goals = int(data["team_away_goals"])
            game.save()
        except:
            return False

        season_team_home = season.season_team_table.filter(team=game.team_home).first()
        season_team_home.matches_played += 1
        season_team_home.goals_scored += game.team_home_goals
        season_team_home.goals_lost += game.team_away_goals
        season_team_away = season.season_team_table.filter(team=game.team_away).first()
        season_team_away.matches_played += 1
        season_team_away.goals_scored += game.team_away_goals
        season_team_away.goals_lost += game.team_home_goals
        
        if game.team_home_goals > game.team_away_goals:
            season_team_home.points += 3
        elif game.team_home_goals < game.team_away_goals:
            season_team_away.points += 3
        else:
            season_team_home.points += 1
            season_team_away.points += 1

        season_team_home.save()
        season_team_away.save()
        
        if season.games.filter(team_home_goals=None).count() == 0:
            season.is_active = False
            season.save()

        return True
    
    return False
