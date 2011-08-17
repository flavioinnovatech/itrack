from django.contrib.sessions.models import Session
from tracking.models import Visitor
from datetime import datetime
from django.http import HttpResponseRedirect


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

class SessionExpiredMiddleware:
    def process_request(request):
        last_activity = request.session['last_activity']
        now = datetime.now()

        if (now - last_activity).minutes > 10:
            # Do logout / expire session
            # and then...
            return HttpResponseRedirect("LOGIN_PAGE_URL")

        if not request.is_ajax():
            # don't set this for ajax requests or else your
            # expired session checks will keep the session from
            # expiring :)
            request.session['last_activity'] = now