import datetime
import math

from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import Event
from .models import Match
from .forms import SchedulerForm
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
    # GET & POST
    context = {}
    context["eventCode"] = code
    context["numTeams"] = teamsCount
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