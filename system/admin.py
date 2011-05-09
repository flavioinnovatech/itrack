from itrack.system.models import System, Settings
from django.contrib import admin

class SettingsInline(admin.StackedInline):
    model = Settings
    extra = 1

class SystemAdmin(admin.ModelAdmin):
    inlines = [SettingsInline]


admin.site.register(System, SystemAdmin)
