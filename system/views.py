from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render_to_response
from itrack.system.models import System, Settings
from django.forms import ModelForm, TextInput
from django.forms.models import modelform_factory
from django.http import HttpResponseRedirect
from django.template.context import RequestContext
from itrack.system.forms import SystemForm, SettingsForm


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
    system = System.objects.filter(administrator__username=request.user.username)
    for item in system:
        parent = item.name
    if parent != []:
        vector = findChild(parent)
    else:
        vector = []

    #code = makelist(vector)
    #print code
    return render_to_response("system/templates/home.html",{ 'user' : request.user, 'system':system, 'vector': vector})

@login_required
@user_passes_test(lambda u: u.groups.filter(name='administradores').count() != 0)
def create_system(request):
    system = System.objects.filter(users__username__exact=request.user.username)
    
    if request.method == 'POST':
        
        form_sett = SettingsForm(request.POST,request.FILES)

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
        form_sett = SettingsForm()

        return render_to_response("system/templates/create_system.html",locals(),context_instance=RequestContext(request),)
		




