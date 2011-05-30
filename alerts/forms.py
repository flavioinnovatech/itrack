# -*- coding: utf-8 -*-

from itrack.alerts.models import Alert
from django.contrib.admin.widgets import *
from django.contrib.auth.models import User
from itrack.system.models import System
from django.template.context import RequestContext
from django.forms import *

class AlertForm(ModelForm):
    class Meta:
        model = Alert
        exclude = ('system')
        widgets = {
            'time_start' : DateTimeInput(attrs={'class':'datepicker'}),
            'time_end': DateTimeInput(attrs={'class':'datepicker'}),
        }
        
    destinataries = ModelMultipleChoiceField(User.objects.all(),widget= FilteredSelectMultiple(u"Notificados",False,attrs={'rows':'30'}))
