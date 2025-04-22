from django.contrib import admin

from .models import Event
from .models import Team

admin.site.register(Event)
admin.site.register(Team)