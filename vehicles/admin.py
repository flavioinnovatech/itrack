from itrack.vehicles.models import Vehicle
from django.contrib import admin


class VehicleAdmin(admin.ModelAdmin):
    pass
    
    
admin.site.register(Vehicle, VehicleAdmin)

