from django.http import HttpResponse
from django.utils import simplejson


def delete(request):
  
  post = request.POST
  print post.id
  name = request.POST.get('id', False)
  
  
  return HttpResponse(name)