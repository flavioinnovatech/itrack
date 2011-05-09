from django.shortcuts import render_to_response
from itrack.system.models import System,Settings

def index(request):
	user_system = System.objects.filter(users__username__exact=request.user.username)
	#system_settings = user_system.
	return render_to_response("templates/themes.html")