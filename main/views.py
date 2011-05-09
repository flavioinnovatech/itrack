from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from itrack.system.models import System

@login_required
def index(request):
    user_system = System.objects.filter(users__username__exact=request.user.username)
    return render_to_response('templates/home.html',{ 'user' : request.user, 'system':user_system})

