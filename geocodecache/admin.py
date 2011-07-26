from itrack.geocodecache.models import CachedGeocode
from django.contrib import admin


#class GeocodeAdmin(admin.ModelAdmin):
#    filter_horizontal = ["custom_fields"]

admin.site.register(CachedGeocode)
