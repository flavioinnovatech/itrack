from django.contrib import auth
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render_to_response
from itrack.accounts.models import UserProfile
from django.contrib.auth.models import User
from django.template.context import Context,RequestContext
from itrack.accounts.forms import UserProfileForm, UserForm
from django.http import HttpResponseRedirect
from itrack.system.models import System, Settings
from django.contrib.auth import authenticate,login
from django.db.models.signals import post_save
from django.dispatch import receiver


@login_required
@user_passes_test(lambda u: u.groups.filter(name='administradores').count() != 0)
def create_user(request):

    #system = System.objects.filter(users__username__exact=request.user.username)
    
    if request.method == 'POST':
        
        form_user = UserForm(request.POST)
        form_profile = UserProfileForm(request.POST)
            
        form_user.save()
        
        if form_user.is_valid():
          new_user = form_user.save(commit=False)
          print new_user.id()
            
        # if form_sett.is_valid():
        #            new_setting = form_sett.save(commit=False)
        #            new_setting.system_id = new_sys.id
        #            new_setting.title = new_sys.name
        #            
        #            new_setting.save()
            # message = "Sistema criado com sucesso."
            #             return render_to_response('system/templates/home.html',locals())
                
        return render_to_response('accounts/templates/create.html',locals(),context_instance=RequestContext(request),)

    else:
        form_user = UserForm()
        form_profile = UserProfileForm()

        return render_to_response("accounts/templates/create.html",locals(),context_instance=RequestContext(request),)
        
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """Create a matching profile whenever a user object is created."""
    if created: 
        profile, new = UserProfile.objects.get_or_create(user=instance)


def login(request):
  
  if request.POST:
    username = request.POST['username']
    password = request.POST['password']
    user = auth.authenticate(username=username, password=password)
    if user is not None and user.is_active:
        # Correct password, and the user is marked "active"
        auth.login(request, user)
        
        system = System.objects.filter(users__username__exact=request.user.username)
        print system
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
        
        print domain
        
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
    
    
    return render_to_response("accounts/templates/home.html",locals())
