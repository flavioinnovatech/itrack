from django.contrib.sessions.models import Session
from tracking.models import Visitor
from datetime import datetime

class UserRestrictMiddleware:

    def process_request(self, request):
        ip_address = request.META.get('REMOTE_ADDR','')
        try:
            last_login = request.user.last_login
        except:
            last_login = 0
        
        if unicode(last_login)[:19] == unicode(datetime.now())[:19]:
            #print 'oi dinovo!>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>'
            
            previous_visitors = Visitor.objects.filter(user=request.user).exclude(ip_address=ip_address)

            for visitor in previous_visitors:
                Session.objects.filter(session_key=visitor.session_key).delete()
                visitor.user = None
                visitor.save()

