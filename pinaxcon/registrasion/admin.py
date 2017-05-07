from django.contrib import admin

import models


@admin.register(models.PastEvent)
class PastEventAdmin(admin.ModelAdmin):
    pass
