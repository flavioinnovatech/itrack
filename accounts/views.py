from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render_to_response
from itrack.accounts.models import UserProfile
from django.contrib.auth.models import User
from django.template.context import RequestContext
from itrack.accounts.forms import UserProfileForm, UserForm
from django.http import HttpResponseRedirect

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
