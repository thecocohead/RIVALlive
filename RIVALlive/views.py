import datetime
import math

from django.http import HttpResponse
from django.shortcuts import render
from .models import Event
from .models import Match
from .forms import SchedulerForm


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

    data = {
        "event" : event,
        "startDate" : startDate,
        "endDate" : endDate,
        "teams" : event.teams.all(),
        "matches" : Match.objects.filter(event=event),
    }

    return render(request, "event.html", data)

def scheduler(request, code):
    teamsCount = Event.objects.get(code=code).teams.all().count()
    form = SchedulerForm(request.POST or None)
    context = {}
    # GET & POST
    context["form"] = form
    context["eventCode"] = code
    context["numTeams"] = teamsCount

    return render(request, "scheduler.html", context)