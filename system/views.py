from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render_to_response
from itrack.system.models import System


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
    print '"'+request.user.username+'"'
    for x in System.objects.all():
        print '"'+x.name+'"'+" : "+'"'+x.administrator.username+'"'
        if x.administrator.username == request.user.username:
            print "Yes!"
        else:
            print "No: "+x.administrator.username,request.user.username
    user_system = System.objects.filter(administrator__username=request.user.username)
    print user_system
    for item in user_system:
        parent = item.name
    if parent != []:
        print "entrou no findChild"
        vector = findChild(parent)
    else:
        vector = []

    code = makelist(vector)
    #print code
    return render_to_response("system/templates/home.html",{ 'user' : request.user, 'system':user_system, 'vector': vector})

@login_required
@user_passes_test(lambda u: u.groups.filter(name='administradores').count() != 0)
def create_system_form(request):
	user_system = System.objects.filter(users__username__exact=request.user.username)
	#TO-DO: criar o form
	return render_to_response("system/templates/create_form.html",{ 'user' : request.user, 'system':user_system})
		
@login_required
@user_passes_test(lambda u: u.groups.filter(name='administradores').count() != 0)
def create_system(request):
	user_system = System.objects.filter(users__username__exact=request.user.username)
		#TO-DO: pegar o request.POST dos dados do sistema, criar um objeto e salvar no banco de dados
	return render_to_response("system/templates/create_form.html",{ 'user' : request.user, 'system':user_system})



