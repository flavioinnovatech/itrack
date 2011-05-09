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
			


@login_required
@user_passes_test(lambda u: u.groups.filter(name='administradores').count() != 0)
def index(request):
	parent = []
	user_system = System.objects.filter(users__username__exact=request.user.username)
	for item in user_system:
		parent = item.name
	if parent != []:
		vector = findChild(parent)
	else:
		vector = []
	return render_to_response("system/templates/home.html",{ 'user' : request.user, 'system':user_system, 'vector': vector})

	@login_required
	@user_passes_test(lambda u: u.groups.filter(name='administradores').count() != 0)
	def create_form(request):
		#TO-DO: criar o form
		return render_to_response("system/templates/create_form.html",{ 'user' : request.user, 'system':user_system})

		@login_required
		@user_passes_test(lambda u: u.groups.filter(name='administradores').count() != 0)
		def create(request):
			#TO-DO: pegar o request.POST dos dados do sistema, criar um objeto e salvar no banco de dados
			return render_to_response("system/templates/create_form.html",{ 'user' : request.user, 'system':user_system})
