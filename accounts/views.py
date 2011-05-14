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