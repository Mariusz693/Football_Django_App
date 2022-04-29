from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import NON_FIELD_ERRORS

from .models import League, Season, Team, User


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


class LeagueUpdateForm(forms.ModelForm):

    class Meta:
        model = League
        fields = ["name", "teams_played"]

    def clean(self, *args, **kwargs):
        
        super().clean(*args, **kwargs)

        if "teams_played" in self.changed_data:
            season_actuall = self.instance.seasons.filter(date_end=None)
            if season_actuall:
                 self.add_error("teams_played", "W trakcie sezonu nie można zmienić liczby drużyn")


class TeamCreateForm(forms.ModelForm):

    class Meta:
        model = Team
        fields = ["name", "country", "actuall_league"]

    def clean(self, *args, **kwargs):
        
        cleaned_data = super().clean(*args, **kwargs)

        if "actuall_league" in self.changed_data:
            league = cleaned_data["actuall_league"]
            if league.teams.count() >= league.teams_played:
                self.add_error("actuall_league", "Liga ma komplet drużyn")
            if cleaned_data["country"] != league.country:
                self.add_error("actuall_league", "Wybrałeś ligę z innego kraju")


class TeamUpdateForm(forms.ModelForm):

    class Meta:
        model = Team
        fields = ["name", "actuall_league"]

    def __init__(self, *args, **kwargs):
        
        super().__init__(*args, **kwargs)

        self.fields["actuall_league"].queryset = League.objects.filter(country=self.instance.country)

    def clean(self, *args, **kwargs):
        
        cleaned_data = super().clean(*args, **kwargs)

        if "actuall_league" in self.changed_data:
            league = cleaned_data["actuall_league"]
            if self.instance.actuall_season:
                self.add_error("actuall_league", "W trakcie sezonu nie można zmienić ligi")
            elif league and league.teams.count() >= league.teams_played:
                self.add_error("actuall_league", "Liga ma komplet drużyn")


class SeasonCreateForm(forms.ModelForm):

    class Meta:
        model = Season
        fields = ["date_start", "league"]
        widgets = {
            "league": forms.HiddenInput(),
            "date_start": DateInput()
        }

    def clean(self, *args, **kwargs):
        
        cleaned_data = super().clean(*args, **kwargs)
        date_start = cleaned_data["date_start"]
        league = cleaned_data["league"]
        season_exists = Season.objects.first()
        # if season_exists:
        #     if season_exists.date_end is None:
        #         self.add_error(NON_FIELD_ERRORS, "Poprzedni sezon nie został jeszcze zakończony")
        #     elif season_exists.date_start.year == date_start.year:
        #         self.add_error(NON_FIELD_ERRORS, "Sezon w tym roku już został stworzony")
        #     elif season_exists.date_start.year > date_start.year:
        #         self.add_error(NON_FIELD_ERRORS, f"Ostatni sezon to {season_exists.season_years}, stwórz kolejny")
        #     elif league.teams.all().count() < league.teams_played:
        #         self.add_error(NON_FIELD_ERRORS, "Za mało drużyn do stworzenia sezonu")
        # elif league.teams.all().count() < league.teams_played:
        #     self.add_error(NON_FIELD_ERRORS, "Za mało drużyn do stworzenia sezonu")
            