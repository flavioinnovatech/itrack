from django.shortcuts import render_to_response
from itrack.system.models import System,Settings

def index(request):

  return render_to_response("templates/rastreamento.html",locals())
