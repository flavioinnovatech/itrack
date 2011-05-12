from django.shortcuts import render_to_response
from itrack.system.models import System
from django.contrib.auth.decorators import login_required

@login_required
def index(request):
	system = System.objects.filter(users__username__exact=request.user.username)
  
	return render_to_response("templates/configgrid.html",locals())