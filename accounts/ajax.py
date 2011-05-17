from django.http import HttpResponse
from django.utils import simplejson
from itrack.accounts.models import UserProfile
from django.contrib.auth.models import User

def delete(request):
  
  post = request.POST.copy()
  i = 0
  
  while(post.has_key("usuarios["+str(i)+"][id]")):
    ids = post["usuarios["+str(i)+"][id]"]
    print ids
    
    user = User.objects.get(pk=ids)
    profile = UserProfile.objects.get(profile=ids)
    
    # Usuario nao pode se auto deletar
    system = request.session['system']    
    users = User.objects.filter(system=system)
    print users
    if (user in users):
      return HttpResponse('falhou')
           
    else:
      user.delete()
      profile.delete()
           
    i = i+1
  
  return HttpResponse('sucesso')