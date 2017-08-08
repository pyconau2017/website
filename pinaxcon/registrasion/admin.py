from django.contrib import admin

from . import models
import registrasion.models.people as rmodels

@admin.register(models.PastEvent)
@admin.register(models.AttendeeProfile)
@admin.register(rmodels.Attendee)
class AttendeeAdmin(admin.ModelAdmin):
    pass
