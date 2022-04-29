"""Football_Project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from football_app import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.IndexView.as_view(), name="index"),
    path('login/', views.LoginView.as_view(), name="login"),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    path('leagues/', views.LeaguesView.as_view(), name="leagues"),
    path('league/<int:pk>/', views.LeagueView.as_view(), name="league"),
    path('league_info/<int:pk>/', views.LeagueInfoView.as_view(), name="league-info"),
    path('league_create/', views.LeagueCreateView.as_view(), name="league-create"),
    path('league_update/<int:pk>/', views.LeagueUpdateView.as_view(), name="league-update"),
    path('league_delete/<int:pk>/', views.LeagueDeleteView.as_view(), name="league-delete"),
    path('season_table/<int:pk>/', views.SeasonTableView.as_view(), name="season-table"),
    path('season_match/<int:pk>/', views.SeasonMatchView.as_view(), name="season-match"),
    path('season_create/<int:pk>/', views.SeasonCreateView.as_view(), name="season-create"),
    path('season_delete/<int:pk>/', views.SeasonDeleteView.as_view(), name="season-delete"),
    
    
    path('teams/', views.TeamsView.as_view(), name="teams"),
    path('team_create/', views.TeamCreateView.as_view(), name="team-create"),
    path('team_seasons/<int:pk>/', views.TeamSeasonsView.as_view(), name="team-seasons"),
    path('team_update/<int:pk>/', views.TeamUpdateView.as_view(), name="team-update"),
    path('team_delete/<int:pk>/', views.TeamDeleteView.as_view(), name="team-delete"),
]
