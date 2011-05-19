from django.shortcuts import render_to_response
from django.conf.urls.defaults import patterns, include, url
from django.contrib.auth.views import login,logout,logout_then_login
from django.conf import settings
from itrack.system.forms import UserCompleteForm, SettingsForm, SystemForm, SystemWizard


# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from dajaxice.core import dajaxice_autodiscover
dajaxice_autodiscover()

urlpatterns = patterns('',
url(r'^$', 'main.views.index'),
url(r'^accounts/login/$', 'accounts.views.login' ),
url(r'^accounts/logout/$', logout_then_login),
url(r'^accounts/$', 'accounts.views.index'),

url(r'^admin/', include(admin.site.urls)),
url(r'^media/(.*)$', 'django.views.static.serve', {'document_root' : settings.MEDIA_ROOT}),
url(r'^accounts/profile/$', 'main.views.index'),
url(r'^themes/$', 'themes.views.index'),

#url(r'^grid/$', 'grid.views.index'),

url(r'^system/$','system.views.index'),
url(r'^system/create/$','system.views.create'),
url(r'^system/edit/(\d+)/$','system.views.edit'),
url(r'^system/delete/(\d+)/$','system.views.delete'),
url(r'^system/create/finish/$','system.views.finish'),

url(r'^rastreamento/veicular/$', 'rastreamento.views.index'),
url(r'^rastreamento/portatil/$', 'rastreamento.views.index'),

url(r'^accounts/create/$', 'accounts.views.create_user'),
url(r'^accounts/edit/(\d+)/$','accounts.views.edit'),
url(r'^accounts/delete/(\d+)/$','accounts.views.delete'),
url(r'^accounts/ajax/delete/$','accounts.ajax.delete'),

(r'^%s/' % settings.DAJAXICE_MEDIA_PREFIX, include('dajaxice.urls')),


)
