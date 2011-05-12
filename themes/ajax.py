from django.utils import simplejson
from dajaxice.core import dajaxice_functions

def myexample(request,text):
	return simplejson.dumps({'message':'%s' % text})

dajaxice_functions.register(myexample)
