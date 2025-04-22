from django.db import models

class Event(models.Model):
    event_name = models.CharField(max_length=200)
    event_id = models.CharField(max_length=200)
    event_start_date = models.DateTimeField("Start Date")
    event_end_date = models.DateTimeField("End Date")

class Team(models.Model):
    team_name = models.CharField(max_length=200)
    team_id = models.CharField(max_length=200)