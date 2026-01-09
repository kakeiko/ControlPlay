from django.contrib import admin
from .models import Rule, Profile, Device, UsageSession

admin.site.register(Rule)
admin.site.register(Profile)
admin.site.register(Device)
admin.site.register(UsageSession)