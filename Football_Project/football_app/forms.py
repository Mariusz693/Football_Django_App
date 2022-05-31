from django import forms
from django.contrib.auth import authenticate

from .models import Season, User


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