from django.contrib import admin
from .models import User, Event, Alert

admin.site.register(User)
admin.site.register(Event)
admin.site.register(Alert)
