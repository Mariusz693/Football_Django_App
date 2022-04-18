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
    path('league_create/', views.LeagueCreateView.as_view(), name="league-create"),
    path('league_table/<int:pk>/', views.LeagueView.as_view(), name="league-table"),
    path('teams/', views.TeamsView.as_view(), name="teams"),
    path('team_create/', views.TeamCreateView.as_view(), name="team-create"),
    path('team_seasons/<int:pk>/', views.TeamSeasonsView.as_view(), name="team-seasons"),
    path('team_update/<int:pk>/', views.TeamUpdateView.as_view(), name="team-update"),
]
