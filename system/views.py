from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render_to_response
from itrack.system.models import System, Settings
from django.forms import ModelForm
from django.forms.models import modelform_factory
from django.http import HttpResponseRedirect
from django.template.context import RequestContext

class SystemForm(ModelForm):
	    class Meta:
	        model = System

class SettingsForm(ModelForm):
    class Meta:
            model = Settings

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

    code = makelist(vector)
    #print code
    return render_to_response("system/templates/home.html",{ 'user' : request.user, 'system':user_system, 'vector': vector})

@login_required
@user_passes_test(lambda u: u.groups.filter(name='administradores').count() != 0)
def create_system(request):
    user_system = System.objects.filter(users__username__exact=request.user.username)
    
    if request.method == 'POST':
        
        form_sett = SettingsForm(request.POST)
        form_sys = SystemForm(request.POST)
        
        print form_sys       
        #if form_sys.is_valid() and form_sett.is_valid:
        #    form_sys.settings = form_sett
        #    form_sys.save()
        return HttpResponseRedirect('/system/')
    else:
        form_sys = modelform_factory(System)
        form_sett = modelform_factory(Settings)
        

        return render_to_response("system/templates/create_system.html",locals(),context_instance=RequestContext(request),)
		




