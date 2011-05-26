from itrack.alerts.models import Alert
from django.forms import *

class AlertForm(ModelForm):
    class Meta:
        model = Alert
        exclude = ('equipment','system')