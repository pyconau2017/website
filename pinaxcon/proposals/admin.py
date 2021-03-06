from django.contrib import admin

import models
from symposion.proposals import models as symposion_models


@admin.register(models.TutorialProposal)
@admin.register(models.PyConAuProposal)

class CategoryAdmin(admin.ModelAdmin):

    class AdditionalSpeakerInline(admin.TabularInline):
        model = symposion_models.AdditionalSpeaker

    inlines = [
        AdditionalSpeakerInline,
    ]
