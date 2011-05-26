from django.shortcuts import render_to_response
from itrack.system.models import System,Settings

def index(request):
  settings = Settings.objects.get(system=request.session["system"])
  if settings.map_google:
    map_google = 1
  if settings.map_maplink:
    map_maplink = 1
  if settings.map_multspectral:
    map_multispectral = 1
    
  return render_to_response("templates/rastreamento.html",locals())
