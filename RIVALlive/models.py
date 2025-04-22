from django.db import models

MATCH_PHASE_CHOICES = {
    "Q": "Qualification",
    "P": "Playoff"
}
MATCH_STATUS_CHOICES = {
    "Schd": "Scheduled",
    "Load": "Loaded",
    "InPr": "In Progress",
    "Rvwg": "Reviewing",
    "Cmpd": "Completed"
}

class Event(models.Model):
    event_name = models.CharField(max_length=200)
    event_code = models.CharField(max_length=200)
    event_start_date = models.DateTimeField("Start Date")
    event_end_date = models.DateTimeField("End Date")
    teams = models.ManyToManyField('Team')

    def __str__(self):
        return self.event_name

class Team(models.Model):
    team_name = models.CharField(max_length=200)
    team_id = models.CharField(max_length=200)
    contact_email = models.CharField(max_length=200)

    def __str__(self):
        return self.team_name

class Match(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="event")
    phase = models.CharField(max_length=200, choices=MATCH_PHASE_CHOICES.items())
    status = models.CharField(max_length=200, choices=MATCH_STATUS_CHOICES.items())
    nbr = models.IntegerField()
    scheduled_time = models.DateTimeField()
    play_time = models.DateTimeField(null=True, blank=True)
    redTeam1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="redTeam1")
    redTeam2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="redTeam2")
    blueTeam1 = models.ForeignKey(Team, on_delete=models.CASCADE,  related_name="blueTeam1")
    blueTeam2 = models.ForeignKey(Team, on_delete=models.CASCADE,  related_name="blueTeam2")
    redScore = models.IntegerField(null=True, blank=True)
    blueScore = models.IntegerField(null=True, blank=True)
    redRP = models.IntegerField(null=True, blank=True)
    blueRP = models.IntegerField(null=True, blank=True)
