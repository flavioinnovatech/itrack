from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from itrack.system.models import System
from django.http import HttpResponseRedirect

@login_required
def index(request):
    return HttpResponseRedirect("/rastreamento/veicular/");
    
def multispectral(request):
  return render_to_response("templates/temp.html",locals())

