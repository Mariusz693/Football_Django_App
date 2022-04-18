from django.shortcuts import render, redirect
from django.views.generic import View, FormView, ListView, CreateView, UpdateView, DetailView
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import League, Season, User, Team
from .forms import LoginForm

# Create your views here.


class IndexView(View):

    """
    Return base page
    """
    def get(self, request):

        return render(
            request,
            "index.html"
        )


class LoginView(FormView):
    """
    Return form to login by admin, patient or employee
    """
    form_class = LoginForm
    template_name = "login.html"

    def get_success_url(self):
    	
        return self.request.GET.get('next') or reverse_lazy('index')


    def form_valid(self, form):

        user = form.authenticate_user()
        
        if user:
            
            login(self.request, user)

        return super().form_valid(form)


class LogoutView(View):
    """
    Return logout view
    """
    def get(self, request):

        if self.request.user.is_authenticated:
            
            logout(request)

        return redirect("index")


class LeaguesView(ListView):
    """
    Return a list of all leagues
    """
    model = League
    template_name = "leagues.html"
    # paginate_by = 10


class LeagueCreateView(LoginRequiredMixin, CreateView):
    """
    Return the add league form view
    """
    model = League
    fields = ["name", "country", "teams_played"]
    template_name = "league_create.html"
    success_url = reverse_lazy("leagues")


class LeagueView(View):

    def get(self, request, pk):

        league = League.objects.get(pk=pk)
        
        return render(
            request,
            "league_table.html",
            context={
                "league": league,
            }
        )


class TeamsView(ListView):
    """
    Return a list of all teams
    """
    model = Team
    template_name = "teams.html"
    # paginate_by = 10


class TeamCreateView(LoginRequiredMixin, CreateView):
    """
    Return the add team form view
    """
    model = Team
    fields = ["name", "country", "actuall_league"]
    template_name = "team_create.html"
    success_url = reverse_lazy("teams")


class TeamSeasonsView(DetailView):
    """
    Return the update team form view
    """
    model = Team
    template_name = "team_seasons.html"


class TeamUpdateView(LoginRequiredMixin, UpdateView):
    """
    Return the update team form view
    """
    model = Team
    fields = ["name", "country", "actuall_league"]
    template_name = "team_update.html"
    
    def get_success_url(self):
        return reverse_lazy("team-seasons", args=(self.object.pk,))