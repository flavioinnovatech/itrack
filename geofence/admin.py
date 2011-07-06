from itrack.geofence.models import Geofence
from django.contrib.gis import admin



admin.site.register(Geofence,admin.GeoModelAdmin)
# admin.site.register(GeoEntity)
