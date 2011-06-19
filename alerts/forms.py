# -*- coding: utf-8 -*-

from itrack.alerts.models import Alert
from itrack.equipments.models import  Equipment,CustomFieldName
from django.contrib.admin.widgets import *
from django.contrib.auth.models import User
from itrack.system.models import System
from django.template.context import RequestContext
from django.forms import *
from itrack.vehicles.models import Vehicle
from itertools import chain
from django.utils.html import escape, conditional_escape

class SpecialSelect(Select):
    def render_option(self, selected_choices, option_value, option_label):
        option_value = force_unicode(option_value)
        selected_html = (option_value in selected_choices) and u' selected="selected"' or ''
        if option_value != '':
            linear_class = (CustomFieldName.objects.get(pk=int(option_value)).custom_field.type == 'LinearInput') and u' class="linearinput"' or ''
        else:
            linear_class = ''
        return u'<option value="%s"%s%s>%s</option>' % (
            escape(option_value), selected_html, linear_class,
            conditional_escape(force_unicode(option_label)))

    def render_options(self, choices, selected_choices):
        # Normalize to strings.
        selected_choices = set([force_unicode(v) for v in selected_choices])
        output = []
        for option_value, option_label in chain(self.choices, choices):
            if isinstance(option_label, (list, tuple)):
                output.append(u'<optgroup label="%s">' % escape(force_unicode(option_value)))
                for option in option_label:
                    output.append(self.render_option(selected_choices, *option))
                output.append(u'</optgroup>')
            else:
                output.append(self.render_option(selected_choices, option_value, option_label))
        return u'\n'.join(output)

class AlertForm(ModelForm):
    class Meta:
        model = Alert
        exclude = ('system')
        widgets = {
            'time_start' : DateTimeInput(attrs={'class':'datepicker'}),
            'time_end': DateTimeInput(attrs={'class':'datepicker'}),
            'state': RadioSelect(),
            'trigger':SpecialSelect(),
        }
    
    vehicle = ModelMultipleChoiceField(Vehicle.objects.all(),widget= FilteredSelectMultiple(u"Veículos",False,attrs={'rows':'30'}))

    destinataries = ModelMultipleChoiceField(User.objects.all(),widget= FilteredSelectMultiple(u"Notificados",False,attrs={'rows':'30'}))
