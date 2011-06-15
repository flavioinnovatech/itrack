from django.forms import *
from itrack.drivers.models import Driver
from itrack.vehicles.models import Vehicle

class DriverForm(ModelForm):
    class Meta:
        model = Driver
        exclude = ('vehicle')


class DriverReallocForm(Form):
    vehicle = ModelChoiceField(Vehicle)


