import datetime
import math

from django.db.models import Q
from django.forms import formset_factory
from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Event
from .models import Match
from .forms import SchedulerForm, ScoreForm
from .scheduler import outerScheduler


def index(request):
    events = Event.objects.order_by('startDate')
    output = []
    for event in events:
        newEvent = {
            "code": event.code,
            "name": event.name,
            "startDate": event.startDate.strftime("%B %d, %Y"),
            "endDate": event.endDate.strftime("%B %d, %Y")
        }
        output.append(newEvent)
    data = {
        "events": output,
    }
    return render(request, 'index.html', data)

def event(request, code):
    event = Event.objects.get(code=code)
    startDate = event.startDate.strftime("%B %d, %Y")
    endDate = event.endDate.strftime("%B %d, %Y")

    context = {
        "event" : event,
        "startDate" : startDate,
        "endDate" : endDate,
        "teams" : event.teams.all(),
        "matches" : Match.objects.filter(event=event),
    }

    # rankings!
    matches = Match.objects.filter(event=event, status="Cmpd")
    teams = event.teams.all()
    rankingInfo = []
    for team in teams:
        teamMatches = matches.filter(Q(redTeam1 = team) | Q(redTeam2 = team) | Q(blueTeam1 = team) | Q(blueTeam2 = team))
        rpTot = 0
        plays = 0
        totalFor = 0
        totalAgainst = 0
        dq = 0
        for match in teamMatches:
            plays += 1
            if any([all([match.redTeam1dq, match.redTeam1 == team]),
                    all([match.redTeam2dq, match.redTeam2 == team]),
                    all([match.blueTeam1dq, match.blueTeam1 == team]),
                    all([match.blueTeam2dq, match.blueTeam2 == team])]):
                # team is disqualified
                dq += 1
            else:
                # count rp
                if any([match.redTeam1 == team, match.redTeam2 == team]):
                    # red alliance
                    rpTot += match.redRP
                    totalFor += match.redScore.getScore()
                    totalAgainst += match.blueScore.getScore()
                else:
                    # blue alliance
                    rpTot += match.blueRP
                    totalFor += match.blueScore.getScore()
                    totalAgainst += match.redScore.getScore()
        # end match calculation
        if plays > 0:
            rpAvg = rpTot / plays
            forAvg = totalFor / plays
            againstAvg = totalAgainst / plays
            # store info
            newEntry = {
                "team": team,
                "RP": rpAvg,
                "forAvg": forAvg,
                "agaAvg": againstAvg,
                "DQs": dq,
                "Plays": plays
            }
        else:
            newEntry = {
                "team": team,
                "RP": -1,
                "forAvg": 0,
                "agaAvg": 0,
                "DQs": dq,
                "Plays": plays
            }
        rankingInfo.append(newEntry)
    # end teams
    context["rankings"] = sorted(rankingInfo, key=lambda x: (-x["RP"], -x["forAvg"], -x["agaAvg"]))

    # process
    for entry in context["rankings"]:
        if entry["RP"] == -1:
            entry["RP"] = "NP"
            entry["forAvg"] = ""
            entry["agaAvg"] = ""
            entry["DQs"] = ""
            entry["Plays"] = ""
        else:
            entry["RP"] = round(entry["RP"], 2)
            entry["forAvg"] = round(entry["forAvg"], 2)
            entry["agaAvg"] = round(entry["agaAvg"], 2)
    return render(request, "event.html", context)

def scheduler(request, code):
    teamsCount = Event.objects.get(code=code).teams.all().count()
    # GET & POST
    context = {}
    context["eventCode"] = code
    context["numTeams"] = teamsCount
    context["currentMatches"] = Match.objects.filter(event=Event.objects.get(code=code)).count()
    context["playedMatches"] = Match.objects.filter(event=Event.objects.get(code=code), status="Cmpd").count()
    form = SchedulerForm()
    if request.method == "GET":
        # GET request
        context["form"] = form
    elif request.method == "POST":
        # POST Request
        responseForm = SchedulerForm(request.POST)
        if responseForm.is_valid():
            outerScheduler(Event.objects.get(code=code), Event.objects.get(code=code).teams.all(), responseForm.cleaned_data["rounds"], responseForm.cleaned_data["cycleTime"],
                           responseForm.cleaned_data["startTime"])
        return redirect(f"/event/{code}")

    return render(request, "scheduler.html", context)

def scoreEntry(request, code, stage, matchNumber):
    context = {}
    context["stage"] = stage
    context["matchNumber"] = matchNumber
    formset = formset_factory(ScoreForm, extra=2)
    formsetReq = formset(request.POST or None)
    context["formset"] = formset

    # get match
    event = Event.objects.get(code=code)
    match = Match.objects.get(event=event, nbr=matchNumber, phase=stage)
    context["redTeam1"] = match.redTeam1
    context["redTeam2"] = match.redTeam2
    context["blueTeam1"] = match.blueTeam1
    context["blueTeam2"] = match.blueTeam2

    # handle POST
    if request.method == "POST":
        if formsetReq.is_valid():
            redScoreForm = formsetReq.forms[0]
            blueScoreForm = formsetReq.forms[1]
            # create models
            redScore = redScoreForm.save()
            blueScore = blueScoreForm.save()
            # calculate out extra rps
            match.redRP = 0
            match.blueRP = 0
            match.redRP = redScore.getRPs()
            match.blueRP = blueScore.getRPs()
            # math!
            if redScore.getScore() > blueScore.getScore():
                # red wins
                match.redRP += 2
            elif blueScore.getScore() > redScore.getScore():
                # blue wins
                match.blueRP += 2
            elif blueScore.getScore() == redScore.getScore():
                # tie
                match.redRP += 1
                match.blueRP += 1
            # process dqs
            if redScore.robot1dq:
                match.redTeam1dq = True
            if redScore.robot2dq:
                match.redTeam2dq = True
            if blueScore.robot1dq:
                match.blueTeam1dq = True
            if blueScore.robot2dq:
                match.blueTeam2dq = True
            # connect up forms
            match.redScore = redScore
            match.blueScore = blueScore
            # mark match as committed
            match.status = "Cmpd"
            # commit
            match.save()
            redScore.save()
            blueScore.save()
        # redirect to next match
        return redirect(f"/event/{code}/scoreEntry/next")

    return render(request, "scoreEntry.html", context)

def nextScoreEntry(request, code):
    matches = Match.objects.filter(event=Event.objects.get(code=code)).filter(status="Schd").order_by("scheduledTime")
    return redirect(f"/event/{code}/scoreEntry/{matches[0].phase}/{matches[0].nbr}")
