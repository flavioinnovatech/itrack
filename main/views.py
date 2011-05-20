from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from itrack.system.models import System

@login_required
def index(request):
    
    return render_to_response('templates/base.html',locals())

