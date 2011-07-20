from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required, user_passes_test
from querystring_parser import parser
from django.http import HttpResponse
from django.utils import simplejson
from django.contrib.gis import geos

from itrack.system.models import System,Settings
from itrack.equipments.models import CustomField,Equipment,Tracking,TrackingData,EquipmentType
from itrack.geofence.models import Geofence
from itrack.alerts.models import Alert
from itrack.paths.forms import PathForm

def index(request):
    form = PathForm(request.session["system"])
    return render_to_response("paths/templates/home.html",locals())
