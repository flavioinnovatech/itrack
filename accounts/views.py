# -*- coding:utf-8 -*-
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
from itrack.system.views import findChild,isChild
from django import forms

def render_user_html(childs,father="",rendered_list=""):
  if childs == []: 
    return ""
  
  if father != "":
    childof = " class='child-of-node-"+str(father)+"' "
  else:
    childof = " class=''"
  
  for x in childs:
      if  type(x).__name__ == "list":
      #if its a list, execute recursively inside it
          parentIndex = childs.index(x) - 1
          father = System.objects.get(pk=childs[parentIndex]).id
          rendered_list+= render_user_html(x,father)
      else:
        #if its a number, mount the url for the system
        #and find the users from the system, and the main admin
          s = System.objects.get(pk=x)
          us = User.objects.filter(system=x)
          
          list_users = []
          list_users.append(s.administrator.id)
          for u in us:
            list_users.append(u.id)
          
          # rendered_list+=System.objects.get(pk=x).name
          rendered_list+=u"<tr style='width:5%;' id=\"node-"+str(x)+"\" "+ childof +"><td style='width:331px;font-weight:bold;text-align:left;'>"+System.objects.get(pk=x).name+" </td><td style='width:150px;text-align:left;padding-left:10px;'>Sistema</td><td style='width:340px;' style='text-align:center;'><a class='table-button' href=\"/accounts/create/"+str(x)+"/\">Criar novo usuario</a> </td></tr>\n"
          
          userfunc = lambda y: y.groups.filter(name='administradores').count() != 0
          posifunc = lambda j,k: j[0] == k
          
          
          for u in list_users:
            
            if userfunc(User.objects.get(pk=u)):
                 usertype = "Administrador"
            else:
                 usertype = "Usuario"
            
            if posifunc(list_users,u):
                erasebutton = ""
            else:
                erasebutton = "<a class='table-button' href=\"/accounts/delete/"+str(u)+"/\" style=\"margin-left:3px;\">&nbsp;Apagar&nbsp;</a>"
              
            rendered_list+=u"<tr style='width:5%;height:24px;'  class='child-of-node-"+str(x)+"'><td style='width:50%; text-align:left;'>"+User.objects.get(pk=u).username+" </td><td style='width:150px;text-align:left;padding-left:10px;'>"+usertype+"</td><td style='text-align:center;'><a class='table-button' href=\"/accounts/edit/"+str(u)+"/\">&nbsp;Editar&nbsp;</a>"+erasebutton+"</td></tr>"

  return rendered_list 


@login_required
@user_passes_test(lambda u: u.groups.filter(name='administradores').count() != 0)
def create_user(request,offset):
    
    if request.method == 'POST':
        
        form_user = UserForm(request.POST)
        form_profile = UserProfileForm(request.POST)
        
        try:
            adm = request.POST['Administrador']
        except:
            adm = None
        
        
        if ( form_user.is_valid() and form_profile.is_valid() ):
          system_id = int(offset)
          system = System.objects.get(pk=int(system_id))
          
          new_user = form_user.save(commit=False)
          
          # Aplica o Hash na senha
          new_user = form_user.save()
          user = User.objects.get(username__exact=new_user)
          password = user.password

          user.set_password(password)
          user.save()
          
          try:
            alert = request.POST["alert"]
          except:
            alert = None
        
          try:
            command = request.POST["command"]
          except:
            command = None
            
          if adm is not None:
            user.groups.add(1)
            
          elif (alert is not None and command is not None) and adm is None:
            user.groups.add(2)
            user.groups.add(3)
            
          elif command is not None and adm is None:
            user.groups.add(3)
            
          elif alert is not None and adm is None:
            user.groups.add(2)
          
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
        #form_user = UserForm()
        #form_profile = UserProfileForm()
        form = UserCompleteForm()
        form.fields["Administrador"] = forms.CharField(widget=forms.CheckboxInput(),help_text="Marque a caixa para atribuir privilégios administrativos ao usuário")
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
        
        print request.user
            
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
        request.session['system_being_created'] = False
        
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
    
    
    rendered_list = render_user_html([system,findChild(system)])
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
        
        try:
            alert = request.POST["alert"]
        except:
            alert = None
            
        try:
          command = request.POST["command"]
        except:
          command = None

        try:
          adm = request.POST['Administrador']
        except:
          adm = None

        
        if adm is not None:
          user.groups.add(1)
          
        elif alert is not None and command is not None:
          user.groups.add(2)
          user.groups.add(3)
          
        elif command is not None:
          user.groups.add(3)
          
        elif alert is not None:
          user.groups.add(2)
        
        new_profile = form_profile.save()
        return HttpResponseRedirect ("/accounts/edit/finish")


    return render_to_response("accounts/templates/edit.html",locals(),context_instance=RequestContext(request))
    
  else:
    
    system = request.session['system']
    users = User.objects.filter(system=system)

    try:
        s = System.objects.get(users__id=user.id)
    except:
        s = System.objects.get(administrator__id = user.id)
    if isChild(s.id,[system,findChild(system)]):
      form = UserCompleteForm(instance = user)
      
      # ROOOTS BLOODY ROOTS
      form.fields["Administrador"] = forms.CharField(widget=forms.CheckboxInput(),help_text="Marque a caixa para atribuir privilégios administrativos ao usuário")
      form.initial = dict( form.initial.items() + profile.__dict__.items())
      form.initial["password"] = ""
      return render_to_response("accounts/templates/edit.html",locals(),context_instance=RequestContext(request))
      
    else:
      return HttpResponseForbidden(u'Você não tem permissão para editar este usuário.')
      
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
    try:
        s = System.objects.get(users__id=user.id)
    except:
        s = System.objects.get(administrator__id = user.id)
        
    if isChild(s.id,[system,findChild(system)]): 
      return render_to_response("accounts/templates/delete.html",locals(),context_instance=RequestContext(request))
      
    else:
      return HttpResponseForbidden(u'Você não tem permissão para deletar este usuário.')      
