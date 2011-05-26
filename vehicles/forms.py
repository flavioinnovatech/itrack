from itrack.vehicles.models import Vehicle
from django.forms import *

class VehicleForm(ModelForm):
    class Meta:
        model = Vehicle
        exclude=['equipment']
