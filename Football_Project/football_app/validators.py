from django.core.exceptions import ValidationError


def validate_teams_count(teams_played):

    if teams_played < 10 or teams_played > 24 or teams_played % 2 == 1:
        raise ValidationError("Liczba drużyn musi być parzysta, min 10, max 24 drużyn")