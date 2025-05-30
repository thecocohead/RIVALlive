from atexit import register

from django.contrib import admin

from .models import Event, ScoreDetail
from .models import Team
from .models import Match

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("code", "name", "startDate", "endDate")

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("number", "name", "contactEmail")

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ("id", "event", "phase", "nbr", "status", "scheduledTime", "playedTime", "redTeam1", "redTeam2", "blueTeam1", "blueTeam2", "redScore", "blueScore", "redRP", "blueRP")

@admin.register(ScoreDetail)
class ScoreDetailAdmin(admin.ModelAdmin):
    list_display = ()