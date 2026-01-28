from django.contrib import admin
from .models import Rule, Profile, Device, UsageSession,Logs

admin.site.register(Rule)
admin.site.register(Profile)
admin.site.register(Device)
admin.site.register(UsageSession)
admin.site.register(Logs)