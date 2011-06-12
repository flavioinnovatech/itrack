from itrack.vehicles.models import Vehicle
from itrack.equipments.models import CustomField
from django.forms import *
from django.contrib.admin.widgets import *

class ConfigForm(Form):
    vehicles = ModelMultipleChoiceField(Vehicle.objects.all(),widget= FilteredSelectMultiple("Veiculos",False,attrs={'rows':'30'}))
    custom_fields = ModelMultipleChoiceField(CustomField.objects.all(),widget= FilteredSelectMultiple("Campos",False,attrs={'rows':'30'}))
