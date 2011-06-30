from itrack.vehicles.models import Vehicle
from itrack.equipments.models import Equipment
from django.forms import *

class VehicleForm(ModelForm):
    class Meta:
        model = Vehicle
        exclude=['equipment','system','last_alert_date']
        
class SwapForm(Form):
    equipment = ModelChoiceField(Equipment.objects.all())
