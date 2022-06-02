import json
from django.forms import ValidationError
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, FormView, ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth import login, logout
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import NON_FIELD_ERRORS
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.http  import JsonResponse
from django.db.models import Q
from django.contrib import messages


from .models import Game, League, Season, Team
from .forms import LoginForm, SeasonCreateForm
from .utils import create_season, calculate_points

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


class TeamListView(ListView):
    """
    Return a list of all teams
    """
    model = Team
    template_name = "team_list.html"
    context_object_name = "team_list"
    paginate_by = 10

    def get_queryset(self):

        team_list = Team.objects.all()
        self.country_list = []
        
        for team in team_list:
            if not team.country in self.country_list:
                self.country_list.append(team.country)
        
        self.search = self.request.GET.get("search")
        self.country = self.request.GET.get("country")
        
        if self.search:
            
            return team_list.filter(name__istartswith=self.search)
        
        if self.country:
            
            return team_list.filter(country=self.country)
    
        return team_list

    def get_context_data(self, *args, **kwargs):
        
        context = super().get_context_data(*args, **kwargs)
        context["country_list"] = self.country_list
        context["search"] = self.search
        context["country"] = self.country
        
        return context


class TeamView(View):
    """
    Return a team info or team table view
    """
    def get(self, request, pk):
        
        team = Team.objects.get(pk=pk)
        
        if team.seasons.first():
        
            return redirect(reverse_lazy("team-table", args=(team.pk, team.seasons.first().pk,)))
        
        else:
        
            return redirect(reverse_lazy("team-info", args=(team.pk,)))


class TeamInfoView(DetailView):
    """
    Return the team info view
    """
    model = Team
    template_name = "team_info.html"
    context_object_name = "team"


class TeamCreateView(LoginRequiredMixin, CreateView):
    """
    Return the add team form view
    """
    model = Team
    fields = ["name", "country"]
    template_name = "team_create.html"
    success_url = reverse_lazy("team-create")
        
    def form_valid(self, form):
        
        self.object = form.save()
        messages.success(self.request, message=self.object.name, extra_tags=self.object.pk)
        
        return super().form_valid(form)


class TeamUpdateView(LoginRequiredMixin, UpdateView):
    """
    Return the update team form view
    """
    model = Team
    fields = ["name"]
    template_name = "team_update.html"
    context_object_name = "team"
    
    def get_success_url(self):

        return reverse_lazy("team-info", args=(self.object.pk,))


class TeamDeleteView(LoginRequiredMixin, DeleteView):
    """
    Return the delete team form view
    """
    model = Team
    template_name = "team_delete.html"
    context_object_name = "team"
    success_url = reverse_lazy("team-list")
    
    def form_valid(self, form):

        if self.object.seasons.filter(is_active=True):
            form.add_error(NON_FIELD_ERRORS, "W trakcie trwającego sezonu nie można usunąć drużyny")
            
            return self.form_invalid(form)

        return super().form_valid(form)


class TeamTableView(DetailView):
    """
    Return a list of league seasons
    """
    model = Team
    template_name = "team_table.html"
    context_object_name = "team"
    
    def get_context_data(self, *args, **kwargs):
        
        context = super().get_context_data(*args, **kwargs)
        season = get_object_or_404(Season, pk=self.kwargs["pk_season"])
        context["season"] = season
        context["next"] = Season.objects.filter(
            season_teams=self.object,
            date_start__gt=season.date_start
            ).last()
        context["prev"] = Season.objects.filter(
            season_teams=self.object,
            date_start__lt=season.date_start
            ).first()
        
        return context


class TeamMatchView(DetailView):
    """
    Return a list of league seasons
    """
    model = Team
    template_name = "team_match.html"
    context_object_name = "team"
    
    def get_context_data(self, *args, **kwargs):
        
        context = super().get_context_data(*args, **kwargs)
        season = get_object_or_404(Season, pk=self.kwargs["pk_season"])
        context["season"] = season
        context["next"] = Season.objects.filter(
            season_teams=self.object,
            date_start__gt=season.date_start
            ).last()
        context["prev"] = Season.objects.filter(
            season_teams=self.object,
            date_start__lt=season.date_start
            ).first()
        context["match_list"] = Game.objects.filter(season=season).filter(
            Q(team_home=self.object)|Q(team_away=self.object)
        )

        return context


class LeagueListView(ListView):
    """
    Return a list of all leagues
    """
    model = League
    template_name = "league_list.html"
    context_object_name = "league_list"
    paginate_by = 10

    def get_queryset(self):

        league_list = League.objects.all()
        self.country_list = []
        
        for league in league_list:
            if not league.country in self.country_list:
                self.country_list.append(league.country)
        
        self.search = self.request.GET.get("search")
        self.country = self.request.GET.get("country")
        
        if self.search:
        
            return league_list.filter(name__icontains=self.search)
        
        if self.country:
        
            return league_list.filter(country=self.country)
    
        return league_list

    def get_context_data(self, *args, **kwargs):
        
        context = super().get_context_data(*args, **kwargs)
        context["country_list"] = self.country_list
        context["search"] = self.search
        context["country"] = self.country
        
        return context


class LeagueView(View):
    """
    Return a league info or league table view
    """
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
    context_object_name = "league"


class LeagueCreateView(LoginRequiredMixin, CreateView):
    """
    Return the add league form view
    """
    model = League
    fields = ["name", "country", "competition_class"]
    template_name = "league_create.html"
    success_url = reverse_lazy("league-create")

    def form_valid(self, form):
        
        self.object = form.save()
        messages.success(self.request, message=self.object.name, extra_tags=self.object.pk)
        
        return super().form_valid(form)
    

class LeagueUpdateView(LoginRequiredMixin, UpdateView):
    """
    Return the update league form view
    """
    model = League
    fields = ["name"]
    template_name = "league_update.html"
    context_object_name = "league"
    
    def get_success_url(self):
        
        return reverse_lazy("league-info", args=(self.object.pk,))


class LeagueDeleteView(LoginRequiredMixin, DeleteView):
    """
    Return the delete league form view
    """
    model = League
    template_name = "league_delete.html"
    context_object_name = "league"
    success_url = reverse_lazy("league-list")
    
    def form_valid(self, form):
        
        if self.object.seasons.filter(is_active=True):
            form.add_error(NON_FIELD_ERRORS, "W trakcie trwającego sezonu nie można usunąć ligi")
        
            return self.form_invalid(form)
            
        return super().form_valid(form)


class SeasonCreateView(LoginRequiredMixin, CreateView):
    """
    Return a add season to league view
    """
    model = Season
    form_class = SeasonCreateForm
    template_name = "season_create.html"

    def get_success_url(self):
    
        return reverse_lazy("season-table", args=(self.object.pk,))
    
    def get_form(self, *args, **kwargs):
        
        form = super().get_form(*args, **kwargs)
        self.form_visible = True
        self.league = get_object_or_404(League, pk=self.kwargs["pk"])
        
        if self.league.seasons.filter(is_active=True):
            form.errors.update({NON_FIELD_ERRORS: ("Poprzedni sezon nie został jeszcze zakończony",)})
            self.form_visible = False 
        else:
            teams_free = []
            
            for team in Team.objects.filter(country=self.league.country):
                if not team.seasons.filter(is_active=True):
                    teams_free.append(team.pk)
            
            teams = Team.objects.filter(pk__in=teams_free)
            form.fields["league"].initial = self.league
            form.fields["season_teams"].queryset = teams
            
            if teams.count() < 10:
                form.errors.update({NON_FIELD_ERRORS: ("Za mało drużyn w kraju do stworzenia ligi, min. 10",)})
                self.form_visible = False
        
        return form

    def get_context_data(self, *args, **kwargs):
        
        context = super().get_context_data(*args, **kwargs)
        context["league"] = self.league
        context["form_visible"] = self.form_visible

        return context
    
    def form_valid(self, form):
        
        season_teams = form.cleaned_data['season_teams']
        number_of_teams = form.cleaned_data['number_of_teams']
        date_start = form.cleaned_data["date_start"]
        season_exists = self.league.seasons.first()
        
        if number_of_teams != season_teams.count():
            form.add_error(NON_FIELD_ERRORS, f"Wybierz odpowiednią liczbę drużyn - {number_of_teams}")
        
        if season_exists and season_exists.date_start.year >= date_start.year:
            form.add_error("date_start", f"Ostatni sezon to {season_exists.season_years}, stwórz kolejny")
        
        self.object = form.save()
        
        try:
            create_season(season=self.object)
        except ValidationError as e:
            form.add_error(NON_FIELD_ERRORS, e)
        
        if form.errors:
            
            return self.form_invalid(form)
        
        return super().form_valid(form)


class SeasonDeleteView(LoginRequiredMixin, DeleteView):
    """
    Return the delete season form view
    """
    model = Season
    template_name = "season_delete.html"
    
    def get_success_url(self):
        
        return reverse_lazy("league-info", args=(self.object.league.pk,))

    def form_valid(self, form):
        
        if self.object.is_active == True:
            form.add_error(NON_FIELD_ERRORS, "W trakcie trwającego sezonu nie można go usunąć")
            
            return self.form_invalid(form)
            
        return super().form_valid(form)


class SeasonTableView(DetailView):
    """
    Return a season table view
    """
    model = Season
    template_name = "season_table.html"
    context_object_name = "season"
    
    def get_context_data(self, *args, **kwargs):
        
        context = super().get_context_data(*args, **kwargs)
        context["next"] = Season.objects.filter(
            league=self.object.league,
            date_start__gt=self.object.date_start
            ).last()
        context["prev"] = Season.objects.filter(
            league=self.object.league,
            date_start__lt=self.object.date_start
            ).first()

        return context


class SeasonMatchView(ListView):
    """
    Return a seasons match view
    """
    model = Game
    template_name = "season_match.html"
    context_object_name = "match_list"

    def get_queryset(self, *args, **kwargs):
        
        self.season = get_object_or_404(Season, pk=self.kwargs['pk'])
        self.paginate_by = self.season.number_of_teams/2
        match_list = self.season.games.all()
        
        return match_list
    
    def get_context_data(self, *args, **kwargs):
        
        context = super().get_context_data(*args, **kwargs)
        context['season'] = self.season
        context["next"] = Season.objects.filter(
            league=self.season.league,
            date_start__gt=self.season.date_start
            ).last()
        context["prev"] = Season.objects.filter(
            league=self.season.league,
            date_start__lt=self.season.date_start
            ).first()

        return context


@method_decorator(csrf_exempt, name='dispatch')
class AddGoalsView(View):
    """
    Add points to match view
    """
    def post(self, request):

        data = json.loads(request.body.decode())
        
        if calculate_points(data=data):

            return JsonResponse({'status': "True"}, status=200)

        return JsonResponse({'status': "False"}, status=200)
