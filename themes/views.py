from itrack.system.models import System,Settings
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render_to_response

@login_required
@user_passes_test(lambda u: u.groups.filter(name='administradores').count() != 0)
def index(request):
	user_system = System.objects.filter(users__username__exact=request.user.username)
	
	for item in user_system:
	    temp = item.id
	
	user_settings = Settings.objects.filter(system=4)

<<<<<<< HEAD
	for item in user_settings:
	    temp = item.color_submenu_hover

=======
>>>>>>> 9932996c476ba4065bc30b09dfce42c160060f91
	return render_to_response("templates/themes.html",{ 'user' : request.user, 'system':user_system, 'settings':temp})
