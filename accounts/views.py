from django.contrib import auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render_to_response
from itrack.accounts.models import UserProfile
from django.contrib.auth.models import User
from django.template.context import Context,loader,RequestContext
from itrack.accounts.forms import UserProfileForm, UserForm
from django.http import HttpResponseRedirect
from itrack.system.models import System, Settings
from django.contrib.auth import authenticate,login

@login_required
@user_passes_test(lambda u: u.groups.filter(name='administradores').count() != 0)
def create_user(request):

    #system = System.objects.filter(users__username__exact=request.user.username)
    
    if request.method == 'POST':
        
        return render_to_response('accounts/templates/create.html',locals(),context_instance=RequestContext(request),)

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
        
        request.session['system'] = System.objects.filter(users__username__exact=request.user.username)
        system = request.session['system']
        
        for item in system:
          system_id = item
        
        user_settings = Settings.objects.filter(system=system_id)
        
        print user_settings

      	for item in user_settings:
      	    css = item.css
        
        print item.css
        
        # Redirect to a success page.
        return render_to_response("templates/base.html",locals())
    else:
        # Show an error page
        return HttpResponseRedirect("/")
  else:
    return render_to_response('accounts/templates/login.html',context_instance=RequestContext(request))

