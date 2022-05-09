from django.core.exceptions import ValidationError


def validate_teams_count(teams_played):

    if teams_played < 10 or teams_played > 24 or teams_played % 2 == 1:
        raise ValidationError("Liczba drużyn musi być parzysta, min 10, max 24 drużyn")


def validate_competition_class(competition_class):

    if competition_class < 1 or competition_class > 5:
        raise ValidationError("Klasa rozgrywek może być w zakresie 1 - 5")