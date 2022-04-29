from django.forms import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, FormView, ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import NON_FIELD_ERRORS

from .models import Game, League, Season, User, Team, SeasonTable
from .forms import LoginForm, LeagueUpdateForm, TeamCreateForm, TeamUpdateForm, SeasonCreateForm
from .utils import create_season

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


class LeagueCreateView(LoginRequiredMixin, CreateView):
    """
    Return the add league form view
    """
    model = League
    fields = ["name", "country", "teams_played"]
    template_name = "league_create.html"
    success_url = reverse_lazy("leagues")


class LeagueUpdateView(LoginRequiredMixin, UpdateView):
    """
    Return the update league form view
    """
    model = League
    form_class = LeagueUpdateForm
    template_name = "league_update.html"
    
    def get_success_url(self):
        
        return reverse_lazy("league-info", args=(self.object.pk,))


class LeagueDeleteView(LoginRequiredMixin, DeleteView):
    """
    Return the delete league form view
    """
    model = League
    template_name = "league_delete.html"
    success_url = reverse_lazy("leagues")
    
    def form_valid(self, form):
        if self.object.seasons.filter(date_end=None):
            form.add_error(NON_FIELD_ERRORS, "W trakcie trwającego sezonu nie można usunąć ligi")
            return self.form_invalid(form)
            
        return super().form_valid(form)


class LeagueView(View):

    def get(self, request, pk):
        league = League.objects.get(pk=pk)
        if league.seasons.first():
            return redirect(reverse_lazy("season-table", args=(league.seasons.first().pk,)))
        else:
            return redirect(reverse_lazy("league-info", args=(league.pk,)))


class LeagueInfoView(DetailView):
    """
    Return a list of league seasons
    """
    model = League
    template_name = "league_info.html"


class SeasonTableView(DetailView):
    """
    Return a list of league seasons
    """
    model = Season
    template_name = "season_table.html"
    
    def get_context_data(self, *args, **kwargs):
        
        context = super().get_context_data(*args, **kwargs)
        context["next"] = Season.objects.filter(
            league=self.object.league,
            season_years__startswith=self.object.season_years[5:]
            ).first()
        context["prev"] = Season.objects.filter(
            league=self.object.league,
            season_years__endswith=self.object.season_years[:4]
            ).first()

        return context


class SeasonMatchView(ListView):
    """
    Return a list of league seasons
    """
    model = Game
    template_name = "season_match.html"

    def get_queryset(self, *args, **kwargs):
        self.season = get_object_or_404(Season, pk=self.kwargs['pk'])
        self.paginate_by = self.season.season_table.count()/2
        object_list = self.season.games.all()
        
        return object_list
    
    def get_context_data(self, *args, **kwargs):
        
        context = super().get_context_data(*args, **kwargs)
        context['season'] = self.season
        context["next"] = Season.objects.filter(
            league=self.season.league,
            season_years__startswith=self.season.season_years[5:]
            ).first()
        context["prev"] = Season.objects.filter(
            league=self.season.league,
            season_years__endswith=self.season.season_years[:4]
            ).first()

        return context


class SeasonCreateView(LoginRequiredMixin, CreateView):
    """
    Return a add season to league view
    """
    model = Season
    form_class = SeasonCreateForm
    template_name = "season_create.html"

    def get_success_url(self):
        return reverse_lazy("season-table", args=(self.object.pk,))

    def get_initial(self, *args, **kwargs):
        initial = super().get_initial(*args, **kwargs)
        self.league = get_object_or_404(League, pk=self.kwargs["pk"])
        initial["league"] = self.league

        return initial

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["league"] = self.league

        return context

    def form_valid(self, form):
        self.object = form.save()
        try:
            create_season(season=self.object)
        
        except ValidationError as e:
            form.add_error(NON_FIELD_ERRORS, e)
            return self.form_invalid(form)
        
        return super().form_valid(form)
        

class SeasonDeleteView(LoginRequiredMixin, DeleteView):
    """
    Return the delete league form view
    """
    model = Season
    template_name = "season_delete.html"
    
    def get_success_url(self):
        return reverse_lazy("league-info", args=(self.object.league.pk,))

    def form_valid(self, form):
        if self.object.date_end is None:
            form.add_error(NON_FIELD_ERRORS, "W trakcie trwającego sezonu nie można go usunąć")
            return self.form_invalid(form)
            
        return super().form_valid(form)


class TeamsView(ListView):
    """
    Return a list of all teams
    """
    model = Team
    template_name = "teams.html"


class TeamCreateView(LoginRequiredMixin, CreateView):
    """
    Return the add team form view
    """
    model = Team
    form_class = TeamCreateForm
    template_name = "team_create.html"
    success_url = reverse_lazy("teams")


class TeamSeasonsView(DetailView):
    """
    Return the team seasons view
    """
    model = Team
    template_name = "team_seasons.html"


class TeamUpdateView(LoginRequiredMixin, UpdateView):
    """
    Return the update team form view
    """
    model = Team
    form_class = TeamUpdateForm
    template_name = "team_update.html"
    
    # def get_success_url(self):
    #     return reverse_lazy("team-seasons", args=(self.object.pk,))

    def get_success_url(self):

        return self.request.GET.get('next') or reverse_lazy("team-seasons", args=(self.object.pk,))
    

class TeamDeleteView(LoginRequiredMixin, DeleteView):
    """
    Return the delete team form view
    """
    model = Team
    template_name = "team_delete.html"
    success_url = reverse_lazy("teams")
    
    def form_valid(self, form):

        if self.object.actuall_season:
            form.add_error(NON_FIELD_ERRORS, "W trakcie trwającego sezonu nie można usunąć drużyny")
            return self.form_invalid(form)
            
        return super().form_valid(form)
