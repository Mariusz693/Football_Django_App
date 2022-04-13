from django.core.exceptions import ValidationError


def validate_season(season):
    
    if len(season) != 9:
        raise ValidationError("Sezon nie poprawnie podany, wpisz xxxx/xxxx")
    
    for count, item in enumerate(season):
        if count == 4:
            if item != "/":
                raise ValidationError("Sezon nie poprawnie podany, wpisz xxxx/xxxx")
    
        elif not item.isdigit():
            raise ValidationError("Sezon nie poprawnie podany, wpisz xxxx/xxxx")
    
    if (int(season[5:])-int(season[:4])) != 1:
        raise ValidationError("Sezon nie poprawnie podany, wpisz xxxx/xxxx")
        

def validate_teams_count(teams_played):

    if teams_played < 10 or teams_played > 24 or teams_played % 2 == 1:
        raise ValidationError("Liczba drużyn musi być parzysta, min 10, max 24 drużyn")