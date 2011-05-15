from django.contrib.auth import authenticate,login
from django.shortcuts import render_to_response
from django.template import Context,loader,RequestContext
from django.http import HttpResponseRedirect
from django.contrib import auth
from itrack.system.models import System, Settings

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
          system_id = item
          domain = item.domain
        
        user_settings = Settings.objects.filter(system=system_id)
        
      	for item in user_settings:
      	    css = item.css
        
        request.session['system'] = system_id
        request.session['css'] = css
        request.session['domain'] = domain
        
        print domain
        
        # Redirect to a success page.
        return render_to_response("templates/base.html",locals(),context_instance=RequestContext(request))
    else:
        # Show an error page
        return HttpResponseRedirect("/")
  else:
    return render_to_response('accounts/templates/login.html',context_instance=RequestContext(request))