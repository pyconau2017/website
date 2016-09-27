from django.contrib import admin

import models
from symposion.proposals import models as symposion_models


@admin.register(models.TalkProposal)
@admin.register(models.TutorialProposal)
@admin.register(models.MiniconfProposal)
@admin.register(models.SysAdminProposal)
@admin.register(models.WriteTheDocsProposal)
@admin.register(models.OpenRadioProposal)
@admin.register(models.SecurityProposal)
@admin.register(models.WootconfProposal)
@admin.register(models.KernelProposal)
@admin.register(models.GamesProposal)
@admin.register(models.TestingProposal)
@admin.register(models.KnowledgeProposal)
@admin.register(models.LawProposal)

class CategoryAdmin(admin.ModelAdmin):

    class AdditionalSpeakerInline(admin.TabularInline):
        model = symposion_models.AdditionalSpeaker

    inlines = [
        AdditionalSpeakerInline,
    ]
