# -*- coding: utf-8 -*-
from itertools import chain

from django.contrib.admin.widgets import *
from django.contrib.auth.models import User
from django.db.models import Q
from django.template.context import RequestContext
from django.forms import *
from django.utils.html import escape, conditional_escape

from itrack.alerts.models import Alert
from itrack.equipments.models import  Equipment,CustomFieldName
from itrack.system.tools import findChildInstance, flatten
from itrack.system.models import System
from itrack.vehicles.models import Vehicle

class SpecialSelect(Select):
    def render_option(self, selected_choices, option_value, option_label):
        option_value = force_unicode(option_value)
        selected_html = (option_value in selected_choices) and u' selected="selected"' or ''
        if option_value != '':
            cft = CustomFieldName.objects.get(pk=int(option_value)).custom_field.type
            cf = CustomFieldName.objects.get(pk=int(option_value)).custom_field.tag
            linear_class = ""
            if cf == 'GeoFence':
              linear_class = u'class = geofence'
            elif cft == 'LinearInput':
              linear_class = u' class="linearinput"'
# linear_class = (CustomFieldName.objects.get(pk=int(option_value)).custom_field.type == 'LinearInput') and u' class="linearinput"' or ''
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
        exclude = ['system','sender']
        widgets = {
            'time_start' : DateTimeInput(attrs={'class':'datepicker'}),
            'time_end': DateTimeInput(attrs={'class':'datepicker'}),
            'state': RadioSelect(),
            'trigger':SpecialSelect(),
        }
    
    vehicle = ModelMultipleChoiceField(Vehicle.objects.all(),widget= FilteredSelectMultiple(u"Veículos",False,attrs={'rows':'30'}))
    destinataries = ModelMultipleChoiceField(User.objects.all(),widget= FilteredSelectMultiple(u"Notificados",False,attrs={'rows':'30'}))
    
    def __init__(self,system, *args, **kwargs):
        super(AlertForm,self).__init__(*args,**kwargs)
        
        sys = System.objects.get(pk=system)
        adm_id = sys.administrator.id
        
        childs = findChildInstance(system)
        flatgenerator =  flatten(childs)
        
        flatlist = []
        for i in flatgenerator:
            flatlist.append(i)
        
        destinataries_id = sum(map(lambda x: sum([list(map(lambda y: y.id,x.users.all())),[x.administrator.id]],[]), flatlist),[])
        
        e_set = Equipment.objects.filter(system = system)
        v_set = []
        for e in e_set:
            try:
                v_set.append(Vehicle.objects.get(equipment=e.id).id)
            except:
                pass
        
        self.fields["vehicle"].queryset = Vehicle.objects.filter(id__in=v_set)
        self.fields["vehicle"].label = "Veículo"
        self.fields["trigger"].queryset = CustomFieldName.objects.filter((Q(custom_field__type = 'Input')|Q(custom_field__type = 'LinearInput')) & Q(system = system) & Q(custom_field__availablefields__system = system)).distinct()
        self.fields["trigger"].empty_label = "(selecione o evento)"
        self.fields['destinataries'].queryset=User.objects.filter((Q(system=system) | Q(pk=adm_id)) | Q(pk__in=destinataries_id) )
        if not sys.can_sms:
            del self.fields['receive_sms']
    
    
