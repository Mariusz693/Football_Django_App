from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import NON_FIELD_ERRORS

from .models import Season, Team, User


class DateInput(forms.DateInput):
    
    input_type = 'date'


class LoginForm(forms.Form):

    email = forms.CharField(label='Email', max_length=64, widget=forms.EmailInput())
    password = forms.CharField(label='Hasło', max_length=64, widget=forms.PasswordInput())

    def clean(self, *args, **kwargs):

        super().clean(*args, **kwargs)
        
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        
        user = User.objects.filter(email=email).first()

        if not user:
            self.add_error('email', 'Email nie zarejestrowany w bazie danych')

        if not authenticate(email=email, password=password):
            self.add_error('password', 'Błędne hasło')
            
                
    def authenticate_user(self):

        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        user = authenticate(email=email, password=password)

        return user


class SeasonCreateForm(forms.ModelForm):

    class Meta:
        model = Season
        fields = ["date_start", "league", "number_of_teams", "season_teams"]
        widgets = {
            "league": forms.HiddenInput(),
            "date_start": DateInput(),
            "season_teams": forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        league = kwargs.pop('league')
        super().__init__(*args, **kwargs)
        teams = Team.objects.filter(country=league.country)
        teams_free = []
        for team in teams:
            if not team.seasons.filter(is_active=True):
                teams_free.append(team.pk)
        if teams.filter(pk__in=teams_free).count() < 10:
            self.fields["season_teams"].label = "Brak w bazie minimalnej liczby drużyn do stworzenia sezonu"
        self.fields["season_teams"].queryset = teams.filter(pk__in=teams_free)
    
    def clean(self, *args, **kwargs):
        
        cleaned_data = super().clean(*args, **kwargs)
        date_start = cleaned_data["date_start"]
        league = cleaned_data["league"]
        season_teams = cleaned_data["season_teams"]
        number_of_teams = cleaned_data["number_of_teams"]
        season_exists = league.seasons.first()

        if season_exists and season_exists.is_active:
            self.add_error(NON_FIELD_ERRORS, "Poprzedni sezon nie został jeszcze zakończony")
        else:
            if season_exists and season_exists.date_start.year >= date_start.year:
                self.add_error("date_start", f"Ostatni sezon to {season_exists.season_years}, stwórz kolejny")
            elif number_of_teams < 10 or number_of_teams > 24 or number_of_teams % 2 == 1:
                self.add_error("number_of_teams", "Liczba drużyn musi być parzysta, min 10, max 24 drużyn")
            elif number_of_teams != season_teams.count():
                self.add_error("season_teams", f"Wybierz odpowiednią liczbę drużyn - {number_of_teams}")
            
