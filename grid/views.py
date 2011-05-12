from django.shortcuts import render_to_response
from itrack.system.models import System
from django.contrib.auth.decorators import login_required

def index(request):
	return render_to_response("templates/configgrid.html")