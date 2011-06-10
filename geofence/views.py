# Create your views here.
from django.shortcuts import render_to_response
from itrack.system.models import System,Settings
from itrack.equipments.models import CustomField,Equipment,Tracking,TrackingData,EquipmentType
from django.contrib.auth.decorators import login_required, user_passes_test

def index(request):
    parent = []
    system = System.objects.filter(administrator__username=request.user.username)
    for item in system:
        parent = item.id
    vector = []
    if parent != []:
        childs = findChild(parent)
        vector.append(parent)
        vector.append(childs)
        
        vector_html = render_system_html2(childs)
        
    return render_to_response("system/templates/home.html",locals())
