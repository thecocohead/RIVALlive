import math
from datetime import timedelta
from random import shuffle

from RIVALlive.models import Match


def outerScheduler(event, teams, numRounds, cycleTime, startTime):
    numMatches = math.ceil((numRounds * teams.count())/4)
    matches = []
    for i in range(numMatches):
        matches.append(Match())

    # match setup
    matchNbr = 1
    for match in matches:
        match.event = event
        match.phase = "Q"
        match.status = "Schd"
        match.nbr = matchNbr

        # time
        delta = timedelta(minutes = (cycleTime * (matchNbr-1)))
        time = startTime + delta
        match.scheduledTime = time

        matchNbr += 1
    scheduledMatches = innerScheduler(matches, teams)

    # delete old matches
    Match.objects.filter(event=event).delete()

    # add new matches
    for match in scheduledMatches:
        match.save()

#Matchmaking algorithim
def innerScheduler(matches, teams):
    # as for right now, randomize
    numMatches = len(matches)
    currentMatch = 0
    teamList = list(teams).copy()
    shuffle(teamList)

    matchList = list(matches).copy()
    while currentMatch < numMatches:
        if len(teamList) < 4:
            # regen list
            teamList = list(teams).copy()
            shuffle(teamList)
        # fill in teams
        matchList[currentMatch].redTeam1 = teamList[0]
        matchList[currentMatch].redTeam2 = teamList[1]
        matchList[currentMatch].blueTeam1 = teamList[2]
        matchList[currentMatch].blueTeam2 = teamList[3]
        # remove teams
        del teamList[:4]
        currentMatch += 1

    return matchList