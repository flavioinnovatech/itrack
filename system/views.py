from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render_to_response
from itrack.system.models import System, Settings
from django.forms import ModelForm, TextInput
from django.forms.models import modelform_factory
from django.http import HttpResponseRedirect
from django.template.context import RequestContext

class SystemForm(ModelForm):
	    class Meta:
	        model = System
	        exclude = ('parent')
	        


class SettingsForm(ModelForm):
    class Meta:
            model = Settings
            exclude = ('title','system')
            widgets = {
                'color_site_background' : TextInput(attrs={'class':'color'}),
                'color_table_background' : TextInput(attrs={'class':'color'}),
                'color_menu_gradient_final' : TextInput(attrs={'class':'color'}),
                'color_menu_gradient_inicial' : TextInput(attrs={'class':'color'}),
                'color_menu_gradient_final_hover' : TextInput(attrs={'class':'color'}),
                'color_menu_gradient_inicial_hover': TextInput(attrs={'class':'color'}),
                'color_submenu_gradient_final': TextInput(attrs={'class':'color'}),
                'color_submenu_gradient_inicial': TextInput(attrs={'class':'color'}),
                'color_submenu_hover': TextInput(attrs={'class':'color'}),
                'color_menu_font': TextInput(attrs={'class':'color'}),
                'color_menu_font_hover': TextInput(attrs={'class':'color'}),
                'color_submenu_font': TextInput(attrs={'class':'color'}),
                'color_submenu_font_hover': TextInput(attrs={'class':'color'}),
                'color_table_line_hover': TextInput(attrs={'class':'color'}),
                'color_table_line_font_hover': TextInput(attrs={'class':'color'}),
                'color_table_header': TextInput(attrs={'class':'color'}),
                'color_site_font': TextInput(attrs={'class':'color'}),
                'color_link': TextInput(attrs={'class':'color'}),
            }

def findChild(parent):
	vector = []
	vector.append(parent)
	
	if (System.objects.filter(parent__name=parent).count() == 0):
		return parent
	else:
		v = []
		for x in System.objects.filter(parent__name=parent):
			n = x.name
			
			el = findChild(n)
			v.append(el)
		vector.append(v)
	return vector
			

def makelist(vector):
	
	for item in vector:
		#if (item != "S"):
			#print "Item :"
		#print item
		if (isinstance(item,list)):
			# Achou novo vetor dentro de vetor
			print "filhos"
			print item
			makelist(item)
		else:
			print "pai:"
			print item
			code = 1
			#return code

@login_required
@user_passes_test(lambda u: u.groups.filter(name='administradores').count() != 0)
def index(request):
    parent = []
    user_system = System.objects.filter(administrator__username=request.user.username)
    for item in user_system:
        parent = item.name
    if parent != []:
        vector = findChild(parent)
    else:
        vector = []

    #code = makelist(vector)
    #print code
    return render_to_response("system/templates/home.html",{ 'user' : request.user, 'system':user_system, 'vector': vector})

@login_required
@user_passes_test(lambda u: u.groups.filter(name='administradores').count() != 0)
def create_system(request):
    user_system = System.objects.filter(users__username__exact=request.user.username)
    
    if request.method == 'POST':
        
        form_sett = SettingsForm(request.POST,request.FILES)
        for x in form_sett:
            print x.errors
        if form_sett.is_valid():
            message = "O sistema foi criado com sucesso."
            print form_sett.cleaned_data['system']
        else:
            message =  "Form invalido."    
            return render_to_response('system/templates/create_system.html',locals(),context_instance=RequestContext(request),)
        print message
        form_sys = SystemForm(request.POST)
       

        return render_to_response('system/templates/home.html',locals())
    else:
        form_sys = SystemForm()
        form_sett = SettingsForm(auto_id="color")

        return render_to_response("system/templates/create_system.html",locals(),context_instance=RequestContext(request),)
		




