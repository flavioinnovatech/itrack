# -*- coding: utf-8 -*-

from django.contrib import auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render_to_response
from itrack.accounts.models import UserProfile
from django.contrib.auth.models import User
from django.template.context import Context,RequestContext
from itrack.accounts.forms import UserProfileForm, UserForm
from django.http import HttpResponseRedirect
from itrack.system.models import System, Settings, User
from django.contrib.auth import authenticate,login
from http403project.http import Http403


@login_required
@user_passes_test(lambda u: u.groups.filter(name='administradores').count() != 0)
def create_user(request):
    
    if request.method == 'POST':
        
        form_user = UserForm(request.POST)
        form_profile = UserProfileForm(request.POST)
          
        if ( form_user.is_valid() and form_profile.is_valid() ):
          
          system_id = request.session['system']
          system = System.objects.get(pk=int(system_id))
          
          new_user = form_user.save()
          new_profile = form_profile.save(commit=False)
          new_profile.profile_id = new_user.id
          new_profile.save()
          
          system.users.add(new_user)

          message = "Usuário criado com sucesso."
          
          #TO-DO pegar usarios pelo ID do sistema
          users = User.objects.filter(system=system)
                
          return render_to_response('accounts/templates/home.html',locals(),context_instance=RequestContext(request),)
        else:
          return render_to_response("accounts/templates/create.html",locals(),context_instance=RequestContext(request),)

    else:
        form_user = UserForm()
        form_profile = UserProfileForm()

        return render_to_response("accounts/templates/create.html",locals(),context_instance=RequestContext(request),)
        


def login(request):
  
  if request.POST:
    username = request.POST['username']
    password = request.POST['password']
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        # Correct password, and the user is marked "active"
        auth.login(request, user)
        
        system = System.objects.filter(users__username__exact=request.user.username)
        for item in system:
          system_id = item.id
          domain = item.domain
          system_name = item.name
        
        user_settings = Settings.objects.filter(system__id=system_id)
        print user_settings
      	for item in user_settings:
      	    css = item.css
        
        request.session['system'] = system_id
        request.session['css'] = css
        request.session['domain'] = domain
                
        request.session['system_name'] = system_name
                
        # Redirect to a success page.
        return render_to_response("templates/base.html",locals(),context_instance=RequestContext(request))
    else:
        # Show an error page
        return HttpResponseRedirect("/")
  else:
    return render_to_response('accounts/templates/login.html',locals(),context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u: u.groups.filter(name='administradores').count() != 0)
def index(request):
    
    system = request.session['system']
    
    #TO-DO pegar usarios pelo ID do sistema
    users = User.objects.filter(system=system)
    
    return render_to_response("accounts/templates/home.html",locals())
    
@login_required
@user_passes_test(lambda u: u.groups.filter(name='administradores').count() != 0)
def edit(request,offset):
  
  if request.method == 'POST':
    
    message = u"Usuário editado com sucesso"
    system = request.session['system']
    
    #TO-DO pegar usarios pelo ID do sistema
    users = User.objects.filter(system=system)
    
    return render_to_response("accounts/templates/home.html",locals(),context_instance=RequestContext(request))
    
  else:
    #display the edit form
    user = User.objects.get(pk=int(offset))
    profile = UserProfile.objects.get(profile=int(offset))
    
    system = request.session['system']
    
    users = User.objects.filter(system=system)
    
    if user in users:
      form_user = UserForm(instance = user)
      form_profile = UserProfileForm(instance = profile)
    
      return render_to_response("accounts/templates/edit.html",locals(),context_instance=RequestContext(request))
      
    else:
      raise Http403(u'Você não tem permissão para editar este usuário.')
      
@login_required
@user_passes_test(lambda u: u.groups.filter(name='administradores').count() != 0)
def delete(request,offset):
  if request.method == 'POST':
    
    message = u"Tem certeza que quer deletar?"
    system = request.session['system']
    
    #TO-DO pegar usarios pelo ID do sistema
    users = User.objects.filter(system=system)
    
    return render_to_response("accounts/templates/home.html",locals(),context_instance=RequestContext(request))
    
  else:
    #display the edit form
    user = User.objects.get(pk=int(offset))
    profile = UserProfile.objects.get(profile=int(offset))
    
    system = request.session['system']
    
    users = User.objects.filter(system=system)
    
    if user in users:
      return render_to_response("accounts/templates/delete.html",locals(),context_instance=RequestContext(request))
      
    else:
      raise Http403(u'Você não tem permissão para deletar este usuário.')      
