from django.forms import *
from itrack.drivers.models import Driver
from itrack.vehicles.models import Vehicle
from django.contrib.admin.widgets import *


class DriverForm(ModelForm):
  
    vehicle = ModelMultipleChoiceField(Vehicle.objects.all(),widget= FilteredSelectMultiple("Veiculos",False,attrs={'rows':'30'}),required=False)
    class Meta:
        model = Driver
        exclude = ('system')

    

    # def __init__(self, system, *args, **kwargs):
    #   super(ReportForm, self).__init__(*args, **kwargs)
    #   self.fields['vehicle'].queryset = Vehicle.objects.filter(system=system)

class DriverReallocForm(Form):
    vehicle = ModelMultipleChoiceField(Vehicle.objects.all(),widget= FilteredSelectMultiple("Veiculos",False,attrs={'rows':'30'}))

    def __init__(self, system, *args, **kwargs):
        super(ReportForm, self).__init__(*args, **kwargs)
        self.fields['vehicle'].queryset = Vehicle.objects.filter(system=system)

