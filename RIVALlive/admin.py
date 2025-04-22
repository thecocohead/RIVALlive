from atexit import register

from django.contrib import admin

from .models import Event
from .models import Team
from .models import Match

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ("event_code", "event_name", "event_start_date", "event_end_date")

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("team_id", "team_name", "contact_email")

@admin.register(Match)
class MatchAdmin(admin.ModelAdmin):
    list_display = ("id", "event", "phase", "nbr", "status", "scheduled_time", "play_time", "redTeam1", "redTeam2", "blueTeam1", "blueTeam2", "redScore", "blueScore", "redRP", "blueRP")