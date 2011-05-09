from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render_to_response
from itrack.system.models import System

@login_required
@user_passes_test(lambda u: u.groups.filter(name='administradores').count() != 0)
def index(request):
    user_system = System.objects.filter(administrator__username__exact=request.child.username)
    
    return render_to_response("system/templates/home.html",{ 'user' : request.user, 'system':user_system})
    
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

#@login_required
#@user_passes_test(lambda u: u.groups.filter(name='administradores').count() != 0)    
#def list_systems(request):

#def system_details(request):


