# -*- coding: utf-8 -*-
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render_to_response
from itrack.accounts.models import UserProfile
from django.contrib.auth.models import User
from django.template.context import Context,RequestContext
from itrack.accounts.forms import UserProfileForm, UserForm, UserCompleteForm
from django.http import HttpResponseRedirect
from itrack.system.models import System, Settings, User
from django.contrib.auth import authenticate,login
from http403project.http import Http403
from django.core.context_processors import csrf
from django.contrib.auth.views import password_reset
from itrack.system.views import findChild, render_system_html2



def render_user_html(childs,father="",rendered_list=""):
  if childs == []: 
    return ""
  
  if father != "":
    childof = " class='child-of-node-"+str(father)+"' "
  else:
    childof = ""
  
  for x in childs:
      if  type(x).__name__ == "list":
      #if its a list, execute recursively inside it
          parentIndex = childs.index(x) - 1
          father = System.objects.get(pk=childs[parentIndex]).id
          rendered_list+= render_user_html(x,father)
      else:
        #if its a number, mount the url for the system
        #and find the users from the system, and the main admin
          a = User.objects.filter(system__administrator = x)
          u = User.objects.filter(system=x)
          print u,a
          # rendered_list+=System.objects.get(pk=x).name
          rendered_list+="<tr style='width:5%;' id=\"node-"+str(x)+"\" "+ childof +"><td style='width:50%;'>"+System.objects.get(pk=x).name+": </td><td style='text-align:center;'><a class='table-button' href=\"/system/edit/"+str(x)+"/\">Editar</a>  <a class='table-button' href=\"/system/delete/"+str(x)+"/\">Apagar</a></td></tr>"

  return rendered_list 


@login_required
@user_passes_test(lambda u: u.groups.filter(name='administradores').count() != 0)
def create_user(request):
    
    if request.method == 'POST':
        
        form_user = UserForm(request.POST)
        form_profile = UserProfileForm(request.POST)
          
        if ( form_user.is_valid() and form_profile.is_valid() ):
          system_id = request.session['system']
          system = System.objects.get(pk=int(system_id))
          
          new_user = form_user.save(commit=False)
          
          # Aplica o Hash na senha
          new_user = form_user.save()
          user = User.objects.get(username__exact=new_user)
          password = user.password

          user.set_password(password)
          user.save()

                    
          new_profile = form_profile.save(commit=False)
          new_profile.profile_id = new_user.id
          new_profile.save()
          
          system.users.add(new_user)

          
          users = User.objects.filter(system=system)
                
          return HttpResponseRedirect("/accounts/create/finish")

        else:
          form = UserCompleteForm(request.POST)
          return render_to_response("accounts/templates/create.html",locals(),context_instance=RequestContext(request),)

    else:
        form_user = UserForm()
        form_profile = UserProfileForm()
        form = UserCompleteForm()

        return render_to_response("accounts/templates/create.html",locals(),context_instance=RequestContext(request),)
        
def edit_finish(request):
    return render_to_response("accounts/templates/edit_finish.html",locals())

def create_finish(request):
    return render_to_response("accounts/templates/create_finish.html",locals())
    
def login(request):
  
  if request.POST:
    username = request.POST['username']
    password = request.POST['password']
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        # Correct password, and the user is marked "active"
        auth.login(request, user)
        
        #searches first in the administrators
        try:
            system = System.objects.get(administrator__username = request.user.username)
            system_id = system.id
            domain = system.domain
            system_name = system.name
        except:
        #if the user is not an admin, search in the users     
            system = System.objects.filter(users__username__exact=request.user.username)            

            #if the user doesn't have a system
            if (len(system) == 0):
              erro = u"Usuário não possui sistema associado."
              return render_to_response("accounts/templates/login.html",locals(),context_instance=RequestContext(request),)
            
            for item in system:
                system_id = item.id
                domain = item.domain
                system_name = item.name
            
        user_settings = Settings.objects.filter(system__id=system_id)
      	for item in user_settings:
      	    css = item.css
      	    
      	user = User.objects.get(username__exact=username)
        user_id = user.id
        
        request.session['system'] = system_id
        request.session['css'] = css
        request.session['domain'] = domain
        request.session['username'] = username
        request.session['user_id'] = user_id
        request.session['system_name'] = system_name
                
        # Redirect to a success page.
        return HttpResponseRedirect("/rastreamento/veicular")#render_to_response("templates/base.html",locals(),context_instance=RequestContext(request))
    else:
        # Show an error page
        erro = u"Usuário ou senha incorretos."
        return render_to_response('accounts/templates/login.html',locals(),context_instance=RequestContext(request))
  else:
    return render_to_response('accounts/templates/login.html',locals(),context_instance=RequestContext(request))

@login_required
@user_passes_test(lambda u: u.groups.filter(name='administradores').count() != 0)
def index(request):
    c = {}
    c.update(csrf(request))
    system = request.session['system']
    
    #TO-DO pegar usarios pelo ID do sistema
    
    users = User.objects.filter(system=system)
    
    rendered_list = ""
    
    for item in users:
      
      rendered_list+=u"<tr style='width:5%;' ><td style='width:50%;'>"+item.username+": </td><td><a class='table-button' href=\"/accounts/edit/"+str(item.id)+"/\">Editar</a>  <a class='table-button' href=\"/accounts/delete/"+str(item.id)+"/\">Apagar</a></td></tr>"
    
    
    rendered_list = render_user_html(findChild(system))
    return render_to_response("accounts/templates/home.html",locals(),context_instance=RequestContext(request))
    
@login_required
@user_passes_test(lambda u: u.groups.filter(name='administradores').count() != 0)
def edit(request,offset):
  
  user = User.objects.get(pk=int(offset))
  profile = UserProfile.objects.get(profile=int(offset))
  if request.method == 'POST':
    form = UserCompleteForm(request.POST,instance=user)
    form_user = UserForm(request.POST, instance = user)
    form_profile = UserProfileForm(request.POST, instance = profile)
    
    
    if form_user.is_valid() and form_profile.is_valid():
        new_user = form_user.save(commit=False)
        new_user.set_password(new_user.password)
        new_user.save()
        new_profile = form_profile.save()
        return HttpResponseRedirect ("/accounts/edit/finish")


    return render_to_response("accounts/templates/edit.html",locals(),context_instance=RequestContext(request))
    
  else:
    
    system = request.session['system']
    users = User.objects.filter(system=system)
        
    if user in users or user.username == request.user.username:
      form = UserCompleteForm(instance = user)
      form.initial = dict( form.initial.items() + profile.__dict__.items())
      
      return render_to_response("accounts/templates/edit.html",locals(),context_instance=RequestContext(request))
      
    else:
      raise Http403(u'Você não tem permissão para editar este usuário.')
      
@login_required
@user_passes_test(lambda u: u.groups.filter(name='administradores').count() != 0)
def delete(request,offset):
  if request.method == 'POST':
    
    user = User.objects.get(pk=int(offset))
    profile = UserProfile.objects.get(profile=int(offset))
    
    profile.delete()
    user.delete()
    
    system = request.session['system']
    
    #TO-DO pegar usarios pelo ID do sistema
    users = User.objects.filter(system=system)
    
    return render_to_response("accounts/templates/delete_finish.html",locals(),context_instance=RequestContext(request))
    
  else:
    user = User.objects.get(pk=int(offset))
    profile = UserProfile.objects.get(profile=int(offset))
    
    system = request.session['system']
    users = User.objects.filter(system=system)
    
    if user in users:
      return render_to_response("accounts/templates/delete.html",locals(),context_instance=RequestContext(request))
      
    else:
      raise Http403(u'Você não tem permissão para deletar este usuário.')      
