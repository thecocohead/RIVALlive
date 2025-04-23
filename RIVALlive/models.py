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
    name = models.CharField(max_length=200)
    code = models.CharField(max_length=200)
    startDate = models.DateTimeField("Start Date")
    endDate = models.DateTimeField("End Date")
    teams = models.ManyToManyField('Team')

    def __str__(self):
        return self.name

class Team(models.Model):
    name = models.CharField(max_length=200)
    number = models.CharField(max_length=200)
    contactEmail = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Match(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="event")
    phase = models.CharField(max_length=200, choices=MATCH_PHASE_CHOICES.items())
    status = models.CharField(max_length=200, choices=MATCH_STATUS_CHOICES.items())
    nbr = models.IntegerField()
    scheduledTime = models.DateTimeField()
    playedTime = models.DateTimeField(null=True, blank=True)
    redTeam1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="redTeam1")
    redTeam2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="redTeam2")
    blueTeam1 = models.ForeignKey(Team, on_delete=models.CASCADE,  related_name="blueTeam1")
    blueTeam2 = models.ForeignKey(Team, on_delete=models.CASCADE,  related_name="blueTeam2")
    redScore = models.IntegerField(null=True, blank=True)
    blueScore = models.IntegerField(null=True, blank=True)
    redRP = models.IntegerField(null=True, blank=True)
    blueRP = models.IntegerField(null=True, blank=True)
