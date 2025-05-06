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

class ScoreDetail(models.Model):
    nearL0normalMissile = models.IntegerField(verbose_name="Near L0 Missiles", default=0)
    nearL0bonusMissile = models.IntegerField(verbose_name="Near L0 Nukes", default=0)
    nearL1normalMissile = models.IntegerField(verbose_name="Near L1 Missiles", default=0)
    nearL1bonusMissile = models.IntegerField(verbose_name="Near L1 Nukes", default=0)
    nearL2normalMissile = models.IntegerField(verbose_name="Near L2 Missiles", default=0)
    nearL2bonusMissile = models.IntegerField(verbose_name="Near L2 Nukes", default=0)
    nearL3normalMissile = models.IntegerField(verbose_name="Near L3 Missiles", default=0)
    nearL3bonusMissile = models.IntegerField(verbose_name="Near L3 Nukes", default=0)
    farL0normalMissile = models.IntegerField(verbose_name="Far L0 Missiles", default=0)
    farL0bonusMissile = models.IntegerField(verbose_name="Far L0 Nukes", default=0)
    farL1normalMissile = models.IntegerField(verbose_name="Far L1 Missiles", default=0)
    farL1bonusMissile = models.IntegerField(verbose_name="Far L1 Nukes", default=0)
    farL2normalMissile = models.IntegerField(verbose_name="Far L2 Missiles", default=0)
    farL2bonusMissile = models.IntegerField(verbose_name="Far L2 Nukes", default=0)
    farL3normalMissile = models.IntegerField(verbose_name="Far L3 Missiles", default=0)
    farL3bonusMissile = models.IntegerField(verbose_name="Far L3 Nukes", default=0)
    robot1Fortify = models.BooleanField(verbose_name="Robot 1 Fortify")
    robot2Fortify = models.BooleanField(verbose_name="Robot 2 Fortify")
    penalties = models.IntegerField(verbose_name="Penalties", default=0)
    robot1dq = models.BooleanField(verbose_name="Robot 1 Disqualification")
    robot2dq = models.BooleanField(verbose_name="Robot 2 Disqualification")

    def getEndgameSubscore(self):
        fortifyScore = 5

        fortifyCount = 0
        if(self.robot1Fortify):
            fortifyCount += 1
        if(self.robot2Fortify):
            fortifyCount += 1

        return fortifyScore * fortifyCount

    def getMissileSubscore(self):
        l0Score = 1
        l0BonusScore = 2
        l1Score = 2
        l1BonusScore = 4
        l2Score = 4
        l2BonusScore = 8
        l3Score = 8
        l3BonusScore = 16

        l0Count = self.nearL0normalMissile + self.farL0normalMissile
        l0BonusCount = self.nearL0bonusMissile + self.farL0bonusMissile
        l1Count = self.nearL1normalMissile + self.farL1normalMissile
        l1BonusCount = self.nearL1bonusMissile + self.farL1bonusMissile
        l2Count = self.nearL2normalMissile + self.farL2normalMissile
        l2BonusCount = self.nearL2bonusMissile + self.farL2bonusMissile
        l3Count = self.nearL3normalMissile + self.farL3normalMissile
        l3BonusCount = self.nearL3bonusMissile + self.farL3bonusMissile

        return l0Score * l0Count + l0BonusScore * l0BonusCount + l1Score * l1Count + l1BonusScore * l1BonusCount + l2Score * l2Count + l2BonusScore * l2BonusCount + l3Score * l3Count + l3BonusScore * l3BonusCount

    def getScore(self):
        penaltyScore = -5

        return self.getMissileSubscore() + self.getEndgameSubscore() + penaltyScore * self.penalties


    def getMissileRP(self):
        nearL0 = self.nearL0normalMissile + self.nearL0bonusMissile
        farL0 = self.farL0normalMissile + self.farL0bonusMissile
        nearL1 = self.nearL1normalMissile + self.nearL1bonusMissile
        farL1 = self.farL1normalMissile + self.farL1bonusMissile
        nearL2 = self.nearL2normalMissile + self.nearL2bonusMissile
        farL2 = self.farL2normalMissile + self.farL2bonusMissile
        nearL3 = self.nearL3normalMissile + self.nearL3bonusMissile
        farL3 = self.farL3normalMissile + self.farL3bonusMissile
        if all(num >= 1 for num in [nearL0, farL0, nearL1, farL1, nearL2, farL2, nearL3, farL3]):
            return True
        else:
            return False

    def getFortificationRP(self):
        if self.robot1Fortify and self.robot2Fortify:
            return True
        else:
            return False

    def getRPs(self):
        rp = 0
        if self.getFortificationRP():
            rp += 1
        if self.getMissileRP():
            rp += 1
        return rp

    def __str__(self):
        score = self.getScore()
        return  str(score) + ("*" * self.getRPs())

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
    redScore = models.ForeignKey(ScoreDetail, null=True, on_delete=models.CASCADE, related_name="redScore")
    blueScore = models.ForeignKey(ScoreDetail, null=True, on_delete=models.CASCADE, related_name="blueScore")
    redTeam1dq = models.BooleanField(default=False)
    blueTeam1dq = models.BooleanField(default=False)
    redTeam2dq = models.BooleanField(default=False)
    blueTeam2dq = models.BooleanField(default=False)
    redRP = models.IntegerField(null=True, blank=True)
    blueRP = models.IntegerField(null=True, blank=True)