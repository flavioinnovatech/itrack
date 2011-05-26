from itrack.command.models import Command
from django.forms import *

class CommandForm(ModelForm):
    class Meta:
        model = Command
        exclude = ['time_sent','time_executed','time_received','system','state']
        
