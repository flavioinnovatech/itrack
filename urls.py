from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.views import login,logout,logout_then_login
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'main.views.index'),
    url(r'^accounts/login/$', login , { 'template_name' : 'accounts/templates/login.html' } ),
    url(r'^accounts/logout/$', logout_then_login),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^media/(.*)$', 'django.views.static.serve', {'document_root' : settings.MEDIA_ROOT}),
	url(r'^accounts/profile/$', 'main.views.index'),
    url(r'^themes/$', 'themes.views.index'),
<<<<<<< HEAD
	url(r'^grid/$', 'grid.views.index'),
	url(r'^system/$','system.views.index'),
	url(r'^rastreamento/veicular$', 'rastreamento.views.index'),
	url(r'^rastreamento/portatil$', 'rastreamento.views.index'),
		
		
=======
		url(r'^grid/$', 'grid.views.index'),
		url(r'^system/$','system.views.index'),
		url(r'^rastreamento/veicular$', 'rastreamento.views.index'),		
>>>>>>> 44ee7bd0faeff0ddb64dfc009dbc195bc80f5d01
)
